***** ASTUCES *****

- PAS DE BASE AUTOMATION AVANT ACTION SERVER
- POUR LES BASE AUTOMATION, IL FAUT PARFOIS RELANCER LE SERVEUR

***** Pyton basics *****

** Tests de comparaison **

a = 15
b = 16

if a == b:
  print('okay')
if a != b:
  print('okayy')
if a:
  print('ok')
if not a: #C++ équivalent : !=
  print('oki')

** Print avec valeurs **

repas = "pizza"
boisson = "coca"

print('jai mange une %s et jai bu un %s' % (repas, boisson))




***** Ajouter les data dans le __manifest__.py *****

    'data':        [
        "security/openacademy_security.xml",
        "security/ir.model.access.csv",
        "data/openacademy_data.xml",
        "views/classses_views.xml",
        "views/sessions_views.xml",
        "views/partner_views.xml",
        "wizard/add_attendee_views.xml",
        "report/session_report.xml",
        "views/openacademy_menu.xml",
    ],





***** __init__.py ***** 

# -*- coding: utf-8 -*-
from . import models
from . import wizard





***** Dossier models *****
***** __init___.py *****

# -*- coding: utf-8 -*-
from . import openacademy_classes, openacademy_sessions, openacademy_partner




***** Modèle de base ***** 

from odoo import api, fields, models, exceptions


class Classes(models.Model):
    _name = 'openacademy.class'
    _description = 'Classes'

#Exemple de champ : 

name = fields.Char('Title', required=True) #Name est le champ de base utilisé par la suite pour les référénce, si pas de champ name, on peut rajouter un champ _rec_name = 'nom.du.champ' 
responsible_id = fields.Many2one('res.partner', string='Responsible')
sessions_ids = fields.One2many('openacademy.session', 'course_id', string='Sessions') #La correspondance se fait sur 'course_id' du modèle session
attendee_ids = fields.Many2many('res.partner', string="Atendees")
difficulty = fields.Selection([('0', 'Low'), ('1', 'Medium'), ('2', 'High'),], string='Difficulty')


***** VIEWS ***** 

***** fichier menu *****

<?xml version="1.0" encoding="utf-8"?>
<odoo>
        <data>
        <!--Open Academy App Menu-->
        <menuitem name="Academy"
                id="menu_academy"
                web_icon="openacademy,static/description/icon.png"
                sequence="40"/>

        <menuitem id="menu_classes" name="Classes" parent="menu_academy" sequence="2" action="classes_action"/>

        </data>
</odoo>

***** Fichier du module ***** 

<?xml version="1.0" encoding="utf-8"?>
<odoo>

        #View tree
        <record id="classes_tree_view" model="ir.ui.view">
            <field name="name">openacademy.class.tree</field>
            <field name="model">openacademy.class</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                </tree>
            </field>
        </record>

        #view form
        <record id="course_form_view" model="ir.ui.view">
            <field name="name">openacademy.class.form</field>
            <field name="model">openacademy.class</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <field name="name"/>
                        </group>
                        <notebook>
                            <page string="Sessions" name="sessions">
                                <field name="sessions_ids"/>                            
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        #Lier les vues au menuitem

        <record id="classes_action" model="ir.actions.act_window">
            <field name="name">Classes</field>
            <field name="type">ir.actions.act_window</field>
            <field name="res_model">openacademy.class</field>
            <field name="view_mode">tree,form</field>
        </record>

</odoo>

***** Compute *****

is_student = fields.Boolean(compute='_compute_is_student')
   
def _compute_is_student(self):
    self.is_student = self.env.user.has_group('openacademy.group_student')    




***** Stored compute *****

taken_seats = fields.Float(compute='_compute_taken_seats', store=True)


**** Related fields ***** 

instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True)])
max_student = fields.Integer('Max seats', related='instructor_id.max_student')


***** Domain dans un field ***** 

instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True)]) #res.partner a un champ instructor

***** Constrains/Onchange/Depends *****

    #Onchange se déclenche à la modification dans l'interface et ne bloque pas
    @api.onchange('taken_seats')
    def check_seats(self):
        if self.taken_seats > 5:
            return {'warning': {
                'title':   'Room full',
                'message': 'Too many attendees'
            }}

    #Constrains se déclenche à la sauvegarde et bloque 
    @api.constrains('max_student', 'attendee_ids')
    def _check_seats(self):
        for record in self:
            if record.taken_seats > 5:
                raise exceptions.ValidationError('Too many attendees')

    #ATTENTION : Le constrains se déclenche sur des valeurs stored en bd donc pas les compute (sauf si Stored)


***** Depends ***** 

    @api.depends('taken_seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for rec in self:
            rec.taken_seats = len(rec.attendee_ids) 



***** Inheritance ***** 

***** Classucal inheritance ***** 

#On laisse le nom et la description, un NOUVEAU modèle est créé en se basant sur le inherit pour récupérer les fields et méthodes
class Sessions(models.Model):
    _name = 'openacademy.session'
    _inherit = 'openacademy.class'
    _description = 'Sessions'

***** Extension ***** 

#On retire le name et description, ce noueau modèle remplace l'ancien en lui rajoutant des champs/méthodes
class Partner(models.Model):
    _inherit = 'res.partner'


***** Delegation *****

#La délégation permet d'accéder au champs des enfants
class Books(models.Model):
    _name = 'library.books'
    _description = 'Books'

class book_copy(models.Model):
    _name = 'library.book_copy'
    _description = 'Book copy'
    _inherits = {'library.books': 'book_id'}

    #champ de référénce
    book_id = fields.Many2one('library.books', string="Book", required=True)



***** View inheritance ***** 

        <record id="bookcopy_form_view" model="ir.ui.view">
            <field name="name">library.book_copy.form</field>
            <field name="model">library.book_copy</field>
            <field name="inherit_id" ref="library.books_form_view"/>
            <field name="arch" type="xml">
                <!-- Your fields -->
            </field>
        </record>  

***** xpath ***** 

        <record id="bookcopy_form_view" model="ir.ui.view">
            <field name="name">library.book_copy.form</field>
            <field name="model">library.book_copy</field>
            <field name="inherit_id" ref="library.books_form_view"/>
            <field name="arch" type="xml">

                #1ère solution
                <field name="isbn" position="after">
                    <field name="reference"/>
                </field>

                #2ème solution (xpath)
                <<xpath expr="//field[@name='isbn']" position="after">
                    <field name="reference"/>
                 </xpath>

            </field>
        </record>  


***** View inherit ***** 

#Quand un modèle _inherit d'un autre totalement, il va prendre la vue du premier (exemple : Si book inherit de product, on aura la vue de product)
#Pour forcer une nouvelle vue : 

        <record id="books_tree_view" model="ir.ui.view">
            <field name="name">library.books.tree</field>
            <field name="model">product.product</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="price"/>
                    <field name="isbn"/>
                </tree>
            </field>
        </record>

        <record id="book_action_view_tree" model="ir.actions.act_window.view">
            <field name="view_mode">tree</field>
            <field name="sequence" eval="20"/>
            <field name="view_id" ref="library.books_tree_view"/>
            <field name="act_window_id" ref="library.books_action"/>
        </record>


***** Smart buttons ***** 

        #L'action du smart button doit être mise avant

        <act_window id="action_view_rent" 
            name="Open renters"
            res_model="res.partner"
            view_mode="tree,form"
            domain="[('rent_ids.book_id', 'in', active_ids)]" />   #Le dernier champ ne peut pas être entre ''

<field name="arch" type="xml">
                <form>
                    <sheet>
                        <div class="oe_button_box" name="button_box">
                            <button class="oe_stat_button" 
                                type="action" #type object si la fonction est dans le modèle
                                name="%(action_view_rent)d" #Pas besoin de l'écriture spéciale si la fonction est dans le modèle (type=object)
                                icon="fa-users">
                                <div class="o_stat_info">
                                    <field name="total_renters" class="o_stat_value"/>
                                    <span class="o_stat_text" >
                                        Renters 
                                    </span>
                                </div>
                            </button>                            
                        </div>  

    #Possibilité aussi d'ouvrir le bouton avec un Return : Exemple 

    @api.multi
    def action_view_rent(self):
        self.ensure_one() #Assure 1 seule instance
        reader_ids = self.rental_ids.mapped('customer_id') #mapped permet de récupérer tous les customers ID de tous les rental IDS sans doublons (un peu comme une boucle sur rental_ids)
        return {
            'name':      'Readers of %s' % (self.name),
            'type':      'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain':    [('id', 'in', reader_ids.ids)],
            'target':    'new',
        }  



***** Wizard *****

#Créer un dossier wizard avec un __init__.py, .xml, .py 

***** __init__.py du wizard *****

<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="add_attendees_view_form" model="ir.ui.view">
        <field name="name">openacademy.add_attendees.form</field>
        <field name="model">openacademy.add_attendee</field>
        <field name="arch" type="xml">
            <form string="Add Attendees">
                <group>
                    <field name="session_id"/>
                    <field name="attendee_ids"/>
                </group>
                <footer>
                    <button name="button_add" type="object" string="Add"/> #Fonction à faire dans le .py
                    <button special="cancel" string="Cancel"/>
                </footer>
            </form>
        </field>
    </record>

    #Ajoute l'option au menu Action
    <act_window id="action_add_attendees"
                name="Add Attendees"
                src_model="res.partner"
                res_model="openacademy.add_attendee"
                view_mode="form"
                target="new"
                key2="client_action_multi"/>
</odoo>


***** .py du wizard *****

from odoo import api, exceptions, fields, models

class AddAttendee(models.TransientModel):
    _name = 'openacademy.add_attendee'
    _description = 'Add attendee'

    session_id = fields.Many2one('openacademy.session', string="Session", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    #Récupère les valeurs cochées avant de cliquer sur Action
    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        attendee_ids = self.env.context['active_ids']
        defaults['attendee_ids'] = attendee_ids
        return defaults


    @api.multi
    def button_add(self):
        self.session_id.attendee_ids |= self.attendee_ids
        return {}

***** Access rights ***** 

***** Catégorie de groupes ***** 

        <record model="ir.module.category" id="module_category_open_academy">
            <field name="name">Open Academy</field>
        </record>

***** Groupe ***** 

        #Idéalement il faut faire hériter les groupes entres eux (Le groupe supérieur hérite des droits du groupe inférieur)
        <record id="group_apprentices" model="res.groups">
            <field name="name">Apprentices</field>
            <field name="category_id" ref="openacademy.module_category_open_academy"/>
            <field name="implied_ids" eval="[(6,0,[ref('base.group_user')])]"/>
        </record>

        <record id="group_maesters" model="res.groups">
            <field name="name">Maesters</field>
            <field name="category_id" ref="openacademy.module_category_open_academy"/>
            <field name="implied_ids" eval="[(6,0,[ref('group_apprentices')])]"/>
        </record>

***** CSV pour droits des groupes ***** 

#id : créé ici, id unique. model_id : aller voir les meta data 
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
session_instructor,Session Instructor,model_openacademy_session,group_instructor,1,1,1,1
session_student,Session Student,model_openacademy_session,group_student,1,1,0,0
course_instructor,Course Instructor,model_openacademy_class,group_instructor,1,1,1,1
course_student,Course Student,model_openacademy_class,group_student,1,0,0,0
partner_instructor,Partner Instructor,model_res_partner,group_instructor,1,1,1,1
partner_student,Partner Student,openacademy.model_res_partner,group_student,1,0,0,0


***** RULE ***** 


        <record id="only_instructor_modify" model="ir.rule">
            <field name="name">Instructor modify own session</field>
            <field name="model_id" ref="model_openacademy_session"/>
            <field name="groups" eval="[(4, ref('openacademy.group_instructor'))]"/>
            <field name="perm_read" eval="1"/>
            <field name="perm_write" eval="1"/>
            <field name="perm_create" eval="0"/>
            <field name="perm_unlink" eval="0"/>
            <field name="domain_force">
                [('instructor_id','=',user.partner_id.id)]
            </field>
        </record>

***** Rendre un champ readonly en fonction du groupe *****

#1 Créer un booléen et un compute : 

    is_student = fields.Boolean(compute='_compute_is_student')

    def _compute_is_student(self):
        self.is_student = self.env.user.has_group('openacademy.group_student')   

#2 On modifie le champ dans la vue en fonction du booléen : 

    <field name="is_student" invisible="1"/> #Le champ doit être présent en invisible
    <field name="name" attrs="{'readonly': [('is_student', '=', True)]}"/>

    #Mettre un champ invisible SI

    <field name="name" attrs="{'invisible': [('is_student', '=', True)]}"/>

***** Chatter ***** 

                   <div class="oe_chatter">
                        <field name="message_follower_ids" widget="mail_followers"/>
                        <field name="message_ids" widget="mail_thread"/>
                    </div>
                </form>
            </field>
        </record>

  
    @api.multi
    def _draft_to_confirmed(self):
        for record in self:
            if (record.taken_seats / record.max_student) > 0.5 and record.state == 'draft':
                record.state = 'confirmed'
                record.message_post(body="Session changed to confirmed") #Ligne qui écrit dans le chatter (Alternative : Attribut track_visibility possible)
      



***** Override de la fonction write *****

    #La fonction write va déclencher la fonction _draft_to_confirmed()
    @api.multi
    def write(self, values):
        result = super(Sessions,self).write(values)
        if 'attendee_ids' in values or 'max_student' in values:
            self._draft_to_confirmed()
        return result



***** Création invoice *****


    <button name="create_invoice" type="object" string="Create invoice" attrs="{'invisible' : [('is_paid', '=', True)]}" />

    @api.multi
    def create_invoice(self):
        self.AccountInvoice = self.env['account.invoice']

        #On vérifie si une invoice existe déjà pour ce partner
        self.invoice = self.AccountInvoice.search([
            ('partner_id', '=', self.instructor_id.id)
        ], limit=1)

        if not self.invoice:
            self.invoice = self.AccountInvoice.create({
                'partner_id': self.instructor_id.id,
            })  

        expense_account = self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)], limit=1)
        self.env['account.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'product_id': self.product_id.id,
            'price_unit': self.product_id.lst_price,
            'account_id': expense_account.id,
            'name':       'Session',
            'quantity':   1,
        })

        self.write({'is_paid': True})


***** Plusieurs conditions dans attrs ***** 

#ET et OU en fonction de si il y a '|'

<field name="instructor_id" attrs="{'readonly': ['|', ('can_edit_instructor', '=', True), ('is_student', '=', True)]}"/>

<field name="instructor_id" attrs="{'readonly': [('can_edit_instructor', '=', True), ('is_student', '=', True)]}"/>


('can_edit_instructor', '=', True), ('|', ('can_edit_instructor', '=', True), ('is_student', '=', True))


***** Barre states *****

     <field name="arch" type="xml">
         <sheet position="before">
             <header>
                 <field name="book_state" widget="statusbar" nolabel="1"
                        statusbar_visible="available,rented,lost"/>
             </header>

***** Boutons visibles en fonction du state ***** 

    <button name="action_return" states="rented" string="Return" type="object"/>
    <button name="action_lost" states="rented" string="Lost" type="object"/>
    <button name="action_confirm" states="draft" string="Confirm" type="object"/>


***** Reports ***** 

#Créer un dossier report avec un .xml dedans

<?xml version="1.0"?>
<odoo>
    <data>
        #Ajoute l'option report au bouton Action
        <report
            id="action_session_report"
            model="openacademy.session"
            string="Session Report"
            name="openacademy.report_session_template"
            file="openacademy.report_session_template"
            report_type="qweb-pdf" />

    <template id="report_session_template">
        <t t-call="web.html_container">
                <t t-call="web.external_layout">

                    <t t-set="address">
                        <p> OK </p>
                    </t>
                    <div class="page">

                    <!-- Report header content -->
                    <t t-foreach="docs" t-as="doc">
                        <!-- Report row content -->

                        <p> Welcome to <b><span t-field="doc.name"/></b></p>

                        <p> Date : <span t-field="doc.session_date"/></p>
                        <p> List of attendees : </p>
                        <t t-foreach="doc.attendee_ids" t-as="attendee">
                            <li><span t-field="attendee.name"/></li>
                        </t>
                        
                    </t>
                    <!-- Report footer content -->
                    </div>
                </t>
        </t>
    </template>

    #On modifie la template extarnal_layout avec un xpath (External_layout = L'en-tête automatique)
    <template id="external_layout_standard" inherit_id="web.external_layout">
            <xpath expr="" position="inside">
                
            </xpath>
    </template>
        

    </data>
</odoo>


***** Tester les reports ***** 

# 127.0.0.1:8069/report/pdf/report_name/ID_du_modèle
127.0.0.1:8069/report/pdf/openacademy.report_session_template/2 



***** Controllers ***** 

#Exemple de controllers 

from odoo import http

class Books(http.Controller):

#le bout de code dans le controller (http.route) s'exécute quand on est sur le bon URL

    @http.route('/library/books', auth='user', website=True)
    def list(self, **kwargs):
        Book = http.request.env['product.product']
        books = Book.search([('is_book','=',True)])
        return http.request.render('library.book_list_template', {'books': books})

    @http.route('/library/book/<model("product.product"):book>', auth='user', website=True)
    def book(self, book, **kwargs):
        book.is_rented = True
        return http.request.redirect('/library/books')


***** View du controller ***** 

<?xml version="1.0" encoding="utf-8"?>
<odoo>

<template id="book_list_template" name="Book List">
#On utilise le layout déjà créé, notre code se rajoute dans le t-raw = 0
    <t t-call="website.layout">
        <div id="wrap" class="container">
            <h1>Books</h1>
            <t t-foreach="books" t-as="book">
                <a t-att-href="'/library/book/%s' % book.id"><div class="row">
                <span t-field="book.name" />,
                <span t-field="book.isbn" />,
                </div>
                </a>
            </t>
        </div>
    </t>
</template>

</odoo>



////////////////////// ONBOARDING //////////////////////

***** Ajouter un champ *****

#Fichier models/.xml 

<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="x_salestarget" model="ir.model.fields">
        <field name="name">x_salestarget</field>
        <field name="field_description">Sales target</field>
        <field name="ttype">float</field>
        <field name="model_id" ref="base.model_res_partner"/> #XML ID (Metadata depuis model)
    </record>
</odoo>

#Fichier views/.xml 

<?xml version="1.0"?>
<odoo>
    <record id="base_view_partner_form_custom" model="ir.ui.view"> #Le record ID doit être unique
        <field name="name">Sales target form view custom</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/> #EXTERNAL ID (Edit view form)
        <field name="priority" eval="100"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='vat']" position="after">
                <field name="x_salestarget"/>
            </xpath>
        </field>
    </record>
</odoo>

***** Ajouter un bouton ***** 

#Dans le views/.xml

    <record id="sales_order_view_form_custom" model="ir.ui.view">
        <field name="name">Delivery rate button</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="priority" eval="100"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='x_delivery_rate']" position="after">
                <button name="%(rate_calc)d" type="action" string="Get rate"/> #TYPE ACTION ET NOM %(...)d
            </xpath>
        </field>
    </record>

#Dans le actions/.xml

    <?xml version="1.0" encoding="UTF-8"?>
    <odoo>
        <record id="rate_calc" model="ir.actions.server"> #Correspond au nom %(...)d
            <field name="name">Delivery rate calculation</field>
            <field name="model_id" ref="sale.model_sale_order"/>
            <field name="state">code</field>
            <field name="sequence">20</field>
            <field name="code">
    <![CDATA[
            #CODE ICI
    ]]>
            </field>
        </record>
    </odoo>

***** Code action server ***** 

<![CDATA[

price = 0.0
weight = 0.0

for line in record.order_line: 
    if line.product_id.weight:
        weight += line.product_id.weight*line.product_uom_qty

if record.amount_total > 20000:
    price = 0
elif weight > 20:
    price = ((weight-20)*0.5)+40 
elif weight > 10:
    price = 40
else:
    price = 20

record['x_delivery_rate'] = price #ATTENTION : Interdit de faire un record.champ = valeur, il faut faire record['champ'] = valeur


]]>


***** Afficher un warning ***** 

<![CDATA[

raise Warning('Coucou')

]]>


***** Field avec compute ***** 

#ATTENTION : Le code ne fonctionne pas forcément 


    <record id="x_commission_laptop_so" model="ir.model.fields">
        <field name="name">x_commission_laptop</field>
        <field name="field_description">Commission Laptop</field>
        <field name="ttype">float</field>
        <field name="model_id" ref="sale.model_sale_order"/>
        <field eval="False" name="store"/>
        <field name="compute">
<![CDATA[
for r in self:
    laptop_commission = 0.0
    for line in r.order_line:
        product = line.product_id
        if product.categ_id.name == 'Laptop':
            laptop_commission += (product.list_price*line.product_uom_qty)*((product.categ_id.x_commission)/100)
        else:
            if product.categ_id.parent_id.name == 'Laptop':
                laptop_commission += (product.list_price*line.product_uom_qty)*((product.categ_id.x_commission)/100)
    r['x_commission_laptop'] = laptop_commission
]]> 

***** Exemple de field compute n°2 ***** 

    <record id="x_margin_percent" model="ir.model.fields">
        <field name="name">x_margin_percent</field>
        <field name="field_description">Margin Percent</field>
        <field name="ttype">float</field>
        <field name="model_id" ref="sale.model_sale_order_line"/>
        <field eval="False" name="store"/>
        <field name="compute">
<![CDATA[
for r in self:
    margin_value = 0.0
    margin_percent = 0.0
    margin_value = (r.price_unit - r.product_id.standard_price)*r.product_uom_qty
    margin_percent = (margin_value / r.product_id.standard_price)*100
    r['x_margin_percent'] = margin_percent
]]> 
        </field>
    </record>

***** Order line depuis Sale Order ***** 

#Impossible de direct faire sale_order.Order_line mais une fois dans la vue TREE, il reconnait chaque orde line
    <record id="so_margin_tree_custom" model="ir.ui.view">
        <field name="name">Margin tree view custom</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="priority" eval="150"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='order_line']//tree//field[@name='name']" position="after">
                <field name="x_margin_value"/> #Field d'une sale.order.line
            </xpath>
        </field>
    </record>

***** On change field ***** 

    <record id="automation_calculate_shipping_weight" model="base.automation">
        <field name="name">Calculate Package weight in KGS</field>
        <field name="model_id" ref="delivery.model_choose_delivery_package"/>
        <field name="state">code</field>
        <field name="trigger">on_change</field>
        <field name="on_change_fields">x_lbs_weight</field>
        <field name="code"><![CDATA[
if record.x_lbs_weight > 0.00:
    record['shipping_weight'] = record.x_lbs_weight * 0.45359237
            ]]></field>
    </record>

***** Override bouton ***** 

#Dans le views/.xml

    <record id="so_confirm_view_form_custom" model="ir.ui.view">
        <field name="name">Confirm custom button</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="priority" eval="100"/>
        <field name="arch" type="xml">
            <xpath expr="//button[@name='action_confirm']" position="replace">
                <button name="%(confirm_custo)d" type="action" string="CONFIRMM"/>
            </xpath>
        </field>
    </record>

#Dans le actions/.xml 

<record id="confirm_custo" model="ir.actions.server">
            <field name="name">Confirm order</field>
            <field name="model_id" ref="sale.model_sale_order"/>
            <field name="state">code</field>
            <field name="sequence">20</field>
            <field name="code">
<![CDATA[
record.action_confirm()

laptop_commission = 0.0
for line in record.order_line:
    product = line.product_id
    if product.categ_id.name == 'Laptop':
        laptop_commission += (product.list_price*line.product_uom_qty)*((product.categ_id.x_commission)/100)
    else:
        if product.categ_id.parent_id.name == 'Laptop':
            laptop_commission += (product.list_price*line.product_uom_qty)*((product.categ_id.x_commission)/100)
record.user_id.partner_id['x_commissionlaptop'] += laptop_commission

misc_commission = 0.0
for line in record.order_line:
    product = line.product_id
    if product.categ_id.name == 'Misc':
        misc_commission += (product.list_price*line.product_uom_qty)*((product.categ_id.x_commission)/100)
    else:
        if product.categ_id.parent_id.name == 'Misc':
            misc_commission += (product.list_price*line.product_uom_qty)*((product.categ_id.x_commission)/100)
record.user_id.partner_id['x_commissionmisc'] += misc_commission

]]>
            </field>
        </record>

***** Afficher un warning, bloquant 

if CONDITION:
    raise Warning('Nice')


***** Créer un nouveau modèle ***** 

#Création du modèle (Exécuter avant d'ajouter les fields pour que le modèle soit connu ?)

    <record id="margin_warning_model" model="ir.model">
        <field name="name">Margin warning model</field>
        <field name="model">x_margin_warning</field>
    </record>

#Ajout des fields 

    <record id="margin_warning_title_field" model="ir.model.fields">
        <field name="name">x_title</field>
        <field name="ttype">char</field>
        <field name="model_id" ref="coopplanning.margin_warning_model"/>
        <field name="field_description">Title</field>
        <field name="readonly" eval="True"/>
    </record>

    <record id="margin_warning_message_field" model="ir.model.fields">
        <field name="name">x_message</field>
        <field name="ttype">char</field>
        <field name="model_id" ref="coopplanning.margin_warning_model"/>
        <field name="field_description">Message</field>
        <field name="readonly" eval="True"/>
    </record>

#Créer les vues 


    <record id="margin_warning_form_view" model="ir.ui.view">
        <field name="name">coopplanning.x_margin_warning.form</field>
        <field name="model">x_margin_warning</field> #Nom du modèle
        <field name="arch" type="xml">
            <form>
                <field name="x_title"/>
                <field name="x_message"/>
            </form>
        </field>
    </record>


***** Appeler un autre modèle dans une action ***** 

title = "Margin"
message = "Margin too low"

warning = env['x_margin_warning'].create({
    'x_title': title,
    'x_message': message,
}) 

action = {
    'type': 'ir.actions.act_window',
    'view_mode': 'form',
    'view_type': 'form',
    'res_model': 'x_margin_warning',
    'target': 'new',
    'res_id': warning.id, #ID du warning
}


***** Faire apparaitre un modèle avec valeurs ***** 

#Context permet d'avoir des valuers par défaut

context = {
    'default_x_title': "Margin", #default_nom_du_field
    'default_x_message': "Margin too low"
}
action = {
    'type': 'ir.actions.act_window',
    'view_mode': 'form',
    'view_type': 'form',
    'res_model': 'x_margin_warning',
    'target': 'new',
    'context': context
}

#Vue : 

 <record id="margin_warning_form_view" model="ir.ui.view">
        <field name="name">coopplanning.x_margin_warning.form</field>
        <field name="model">x_margin_warning</field>
        <field name="arch" type="xml">
            <form>
                <group> #ATTENTION : si pas de group, pas de label
                    <field name="x_title" string="Title"/>
                    <field name="x_message" string="Message"/>
                </group>
            </form>
        </field>
    </record>

***** Renvoyer une action ***** 

#Dans une actions.server

action = ... 

***** Automated action ***** 

#ATTENTION : INSTALLER BASE AUTOMATION 

    <record id="automation_create_meeting" model="base.automation">
        <field name="name">Add attendee on meeting creation</field>
        <field name="model_id" ref="calendar.model_calendar_event"/>
        <field name="trigger">on_create</field>
        <field name="active" eval="True"/>
        <field name="state">code</field>
        <field name="code">
<![CDATA[
part_id = env['crm.lead'].browse(record.res_id).partner_id
record['partner_ids'] = [(4, part_id.id, 0)]
record['partner_ids'] = [(4, record.user_id.partner_id.id, 0)]
]]>
        </field>
    </record>

**** Ajouter à un dictionnaire ***** 

action['context'] = {
    'default_activity_type_id': record.activity_type_id.id,
    'default_res_id': env.context.get('default_res_id'),
    'default_res_model': env.context.get('default_res_model'),
    'default_name': record.summary or record.res_name,
    'default_description': record.note and tools.html2plaintext(record.note).strip() or '',
    'default_activity_ids': [(6, 0, record.ids)],
}

action['context']['default_partner_ids'] = [(4, part_id.id, 0)]


***** Onchange action *****

#!!!! Le onchange en saas s'effectuent après ceux en standard

<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_payment_onchange" model="base.automation">
        <field name="name">UK Payment term</field>
        <field name="model_id" ref="sale.model_sale_order"/>
        <field name="trigger">on_change</field>
        <field name="on_change_fields">partner_id</field>
        <field name="state">code</field>
        <field name="code">
<![CDATA[
if record.partner_id.country_id.code == 'GB':
    record['payment_term_id'] = env['account.payment.term'].search([('name', '=', "UK payment")])
]]>
        </field>
    </record>
</odoo>


***** CUSTO N°1 : QWEB TEMPLATE *****

<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <template id="tso_website_sale" inherit_id="website_sale.product">
        <xpath expr="//div[@itemprop='description']" position="before">
            <div class="container"> #Permet de s'aligner au reste de la page
                <table class="table table-borderless table-sm">
                    <colgroup> #Gère la width des colonnes
                        <col width="20%" />
                    </colgroup>
                    <tr t-if='product.x_studio_beschreibung_kurz'> #On vérifie si le champ est vide ou pas
                        <td><b><span t-esc="product.fields_get('x_studio_beschreibung_kurz').get('x_studio_beschreibung_kurz').get('string')"/></b></td> #nom du field
                        <td><span t-field="product.x_studio_beschreibung_kurz"/></td>
                    </tr> 
                    <tr t-if='product.x_studio_beschreibung_lang_1'>
                        <td><b><span t-esc="product.fields_get('x_studio_beschreibung_lang_1').get('x_studio_beschreibung_lang_1').get('string')" /></b></td>
                        <td><span t-field="product.x_studio_beschreibung_lang_1"/></td>
                    </tr>
                    <tr t-if='product.x_studio_ort'>
                        <td><b><span t-esc="product.fields_get('x_studio_ort').get('x_studio_ort').get('string')"/></b></td>
                        <td><span t-field="product.x_studio_ort"/></td>
                    </tr>
                    <tr t-if='product.x_studio_verfgbarkeit'>
                        <td><b><span t-esc="product.fields_get('x_studio_verfgbarkeit').get('x_studio_verfgbarkeit').get('string')"/></b></td>
                        <td><span t-field="product.x_studio_verfgbarkeit"/></td>
                    </tr>
                    <tr t-if='product.x_studio_dauer'>
                        <td><b><span t-esc="product.fields_get('x_studio_dauer').get('x_studio_dauer').get('string')"/></b></td>
                        <td><span t-field="product.x_studio_dauer"/></td>
                    </tr>
                    <tr t-if='product.x_studio_teilnehmer'>
                        <td><b><span t-esc="product.fields_get('x_studio_teilnehmer').get('x_studio_teilnehmer').get('string')"/></b></td>
                        <td><span t-field="product.x_studio_teilnehmer"/></td>
                    </tr>
                    <tr t-if='product.x_studio_kosten'>
                        <td><b><span t-esc="product.fields_get('x_studio_kosten').get('x_studio_kosten').get('string')"/></b></td>
                        <td><span t-field="product.x_studio_kosten"/></td>
                    </tr>
                </table>
            </div>
        </xpath>
    </template>

</odoo>

** Création account.account **

new_account = env['account.account'].create({
    'code': '69000',
    'name': 'Auxiliary - Test Account',
    'user_type_id': env.ref('account_reports.account_financial_report_other_income0').id, #explicite donc ici il faut mettre .id /// VOIR PLUS BAS POUR LA VALEUR
})
record['x_auxiliary'] = new_account #On fait un = donc pas besoin de new_account.id (même si ça pourrait marcher aussi)

*ATTENTION : Si dans un onchange, pas de create mais un new : *

new_account = env['account.account'].create({
    'code': '69000',
    'name': 'Auxiliary - Test Account',
    'user_type_id': env.ref('account_reports.account_financial_report_other_income0').id,
})
record['x_auxiliary'] = new_account

#Pour trouver le user_type_id :
#Un search :
'user_type_id': env['account.account.type'].search([('name', '=', "Other Income")]).id

#Directement référencer ce qui existe déjà :
'user_type_id': env.ref('account_reports.account_financial_report_other_income0').id

** Check si une valeur est vide **

#ATTENTION :

if not record.x_auxiliary ///DIFFERENT DE //// if record.x_auxiliary == False:

# None =/= not =/= == False


*** Sequence ***

#Définition de la séquence dans le xml :

<record id ="my_sequence_id" model ="ir.sequence">
    <field name ="name">account_seq</field>
    <field name ="code">my_seq</field>  #Code utilisé pour appeler la séquence
    <field name ="padding">3 </field> #Nombre de chiffres, exemple padding 3 = 001, 002, ...
    <field name ="prefix">400 </field> #Avant le chiffre, exemple ici : 400001; 400002, ...
    <field name ="suffix"></field> #après le chiffre
</record>

#Appel de la séquence

record['x_auxiliary'] = env['account.account'].create({
    'code': env['ir.sequence'].next_by_code('my_seq'), #APPEL ICI
    'name': 'Auxiliary account - ' + record.name,
    'user_type_id': env.ref('account_reports.account_financial_report_other_income0').id,
    'x_account_partner_id': record.id,
})


*** Rechercher un élément avec création ***

#Chaque partner a un compte personnalisé, ce compte possède un champ x_account_partner_id pour le lier au partner
#On vérifie si le compte lié au partner existe, si il existe on le set (si ce n'est pas déjà fait) sinon on le créé

    <record id="auxiliary_on_write" model="base.automation">
        <field name="name">Create Auxiliary</field>
        <field name="model_id" ref="base.model_res_partner"/>
        <field name="trigger">on_create_or_write</field>
        <field name="state">code</field>
        <field name="code">
<![CDATA[
if record.company_type == 'company' and not record.x_auxiliary:  #On regarde si le champ est vide, sinon on ne fait rien
    if not env['account.account'].search([('x_account_partner_id', '=', record.id)]): #On cherche si l'élément existe
        record['x_auxiliary'] = env['account.account'].create({ #Si il n'existe pas, on le créé
            'code': env['ir.sequence'].next_by_code('my_seq'),
            'name': 'Auxiliary account - ' + record.name,
            'user_type_id': env.ref('account_reports.account_financial_report_other_income0').id,
            'x_account_partner_id': record.id,
         })
    else: #Si il existe, on le set correctement sur le partner
        record['x_auxiliary'] = env['account.account'].search([('x_account_partner_id', '=', record.id)])

]]>
        </field>
    </record>

*** OVERRIDE BOUTON FACILE ***

#D'abord trouver le bouton pour ça :
    #Regarde sur le bouton et voir son nom ou son ACTION ID
    #Chercher le nom/A_ID dans les vues et inherited vues
    #Regarder depuis quel EXTERNAL ID ça vient puis aller dans le code pour retrouver le vrai nom du bouton

#Si on veut juste modifier l'action d'un bouton ou son nom, pas besoin de position="replace" mais plutôt position="attributes" -> EXEMPLE

    <record id="so_create_invoice_form_custom" model="ir.ui.view">
        <field name="name">Create invoice custom button</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="priority" eval="100"/>
        <field name="arch" type="xml">
#ATTENTION : IL Y AVAIT 2 BOUTONS DONC ON REMPLACE LES DEUX
            <xpath expr="//button[@name='%(sale.action_view_sale_advance_payment_inv)d'][1]" position="attributes">
                <attribute name="name">%(confirm_custo)d</attribute>
                <attribute name="string">CONFIRM</attribute>
            </xpath>
            <xpath expr="//button[@name='%(sale.action_view_sale_advance_payment_inv)d'][1]" position="attributes"> #On remet '[1]' dans le xpath parce que le nom a changé
                <attribute name="name">%(confirm_custo)d</attribute>
                <attribute name="string">CONFIRM</attribute>
            </xpath>
        </field>
    </record>

** Modifier un domain existant **

#ATTENTION : Le xpath/attributes ne va pas supprimer les autres attributes mais va écraser celui qu'on modifie, il faut donc réécrire le domain en entier dans ce cas
    <record id="invoice_account_tree_custom" model="ir.ui.view">
        <field name="name">invoice line view custom</field>
        <field name="model">account.invoice</field>
        <field name="inherit_id" ref="account.invoice_form"/>
        <field name="priority" eval="150"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='invoice_line_ids']//tree//field[@name='account_id']" position="attributes">
                <attribute name="domain">[('user_type_id', '=', 'Income')]</attribute>
            </xpath>
        </field>
    </record>

** Activer une vue Primary **

<group>
    <field name="member_price"/>
    <field name="account_invoice_id" context="{'form_view_ref': 'account.invoice_form'}"/>
</group>

** Valeurs many2one **

#Aller voir dans les External Identifiers
#Trouver la valeur qu'on veut
#Prendre l'identifier et le noter entre %()d

#EXEMPLE :

<xpath expr="//field[@name='invoice_line_ids']//tree//field[@name='account_id']" position="attributes">
    <attribute name="domain">[('user_type_id', '=', 'Income')]</attribute>
</xpath>

#Ici 'Income' est mauvais car peut être traduit, du coup on prend l'identifier ->

    <attribute name="domain">[('user_type_id', '=', %(account.data_account_type_revenue)d)]</attribute>

** With context **

with_context(coucou=True) #Rajoute coucou = True dans le context et le renvoie le context

#ATTENTION !!!!
with_context({'coucou': True}) #ECRASE le context si on lui passe un dictionnaire

** ipdb **

Mettre dans le code :

import ipdb
ipdb.set_trace()

** Pimary view **

#L'objectif d'une Primary View est d'étendre une vue existante sans pour autant la remplacer, on créé une diplication de la vue inherited et on la modifie

        <record id="test_primary_invoice" model="ir.ui.view">
            <field name="model">account.invoice</field>
            <field name="inherit_id" ref="account.invoice_form" />
            <field name="mode">primary</field>
            <field name="arch" type="xml">
                <xpath expr="//field[@name='payment_term_id']" position="before">
                    <field name="x_test_primary" readonly="1"/>
                </xpath>
            </field>
        </record>

#Pour afficher la primary view, il faut la lier à une action
#Exemple ici : On override un bouton et on lui rajoute la valeur 'form_view_ref' dans son contexte avec notre vue

        <div class="oe_button_box" name="button_box">
            <button name="action_view_invoice" type="object" class="oe_stat_button" icon="fa-pencil-square-o" attrs="{'invisible': [('invoice_count', '=', 0)]}">
                <field name="invoice_count" widget="statinfo" string="Invoices"/>
            </button>
        </div>

#DEVIENT --->

        <div class="oe_button_box" name="button_box">
            <button name="422" type="action" context="{'form_view_ref': 'accounting_custo.test_primary_invoice'}" class="oe_stat_button" icon="fa-pencil-square-o" attrs="{'invisible': [('invoice_count', '=', 0)]}">
                <field name="invoice_count" widget="statinfo" string="Invoices"/>
            </button>
        </div>

#On change le nom
#On met type = "Action"
#On rajoute un context

#Voir sale.view_order_form

*** Wizard avec un bouton

* 1 : Créer le modèle *

<odoo>
    <data noupdate="1">
        <record id="variants_cost_wizard_model" model="ir.model">
            <field name="name">Variants cost</field>
            <field name="model">x_variants_cost_wizard</field>
            <field name="transient" eval="True"/>
        </record>
    </data>
</odoo>

* 2 : Ajouter les fields au modèle *

<odoo>
    <data noupdate="1">

        <record id="x_variant_field" model="ir.model.fields">
            <field name="name">x_variant_field</field>
            <field name="ttype">many2one</field>
            <field name="relation">product.product</field>
            <field name="model_id" ref="variants_cost_wizard_model"/>
            <field name="field_description">Variant</field>
            <field name="required" eval="True"/>
        </record>

        <record id="x_dlt_field" model="ir.model.fields">
            <field name="name">x_dlt_field</field>
            <field name="ttype">integer</field>
            <field name="model_id" ref="variants_cost_wizard_model"/>
            <field name="field_description">Delivery lead time</field>
            <field name="required" eval="False"/>
        </record>

    </data>
</odoo>

* 3 : Créer la view form du wizard *

    <record id="view_variants_cost_wizard_model" model="ir.ui.view">
        <field name="name">Add variants cost</field>
        <field name="model">x_variants_cost_wizard</field>
        <field name="arch" type="xml">
            <form>
                <field name="x_variant_field"/>
                <field name="x_supplier_field"/>
                <field name="x_dlt_field"/>
                <field name="x_extra_field"/>
                <field name="x_cost_field"/>
                <footer>
                    <button name="%(variants_cost_wizard_action)d"  string="Add costs" type="action" class="btn-primary"/>
                    <button string="Cancel" class="btn-default" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

#ATTENTION : Bien mettre <form>

* 4 : Créer l action window qui ouvre le wizard *

    <record id="action_view_variants_cost_wizard_model" model="ir.actions.act_window">
        <field name="name">Variants cost</field>
        <field name="type">ir.actions.act_window</field>
        <field name="res_model">x_variants_cost_wizard</field>
        <field name="view_type">form</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>

#Le nom de l'action est liée au bouton

* 5 : Créer le bouton pour afficher le wizard *

    <record id="product_view_wizard_custom" model="ir.ui.view">
        <field name="name">Variant wizard button</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_only_form_view"/>
        <field name="priority" eval="100"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='barcode']" position="after">
                <button name="%(action_view_variants_cost_wizard_model)d" type="action" string="Display Wizard"/>
            </xpath>
        </field>
    </record>

#Le nom du bouton est l'action window qui ouvre le wizard

* 6 : Créer l action quand on valide le wizard *

<?xml version="1.0" encoding="UTF-8"?>
<odoo>

    <record id="variants_cost_wizard_action" model="ir.actions.server">
        <field name="name">Confirm costs</field>
        <field name="model_id" ref="variants_cost_wizard_model"/>
        <field name="state">code</field>
        <field name="sequence">20</field>
        <field name="code">
<![CDATA[
blabla
]]>
        </field>
    </record>
</odoo>

* 6 bis : Ouvrir wizard avec server actions *

#Avantages : Envoyer un contexte par exemple

    <record id="action_view_variants_cost_wizard_model" model="ir.actions.server">
            <field name="name">Display wizrd</field>
            <field name="model_id" ref="variants_cost_wizard_model"/>
            <field name="state">code</field>
            <field name="sequence">20</field>
            <field name="code">
    <![CDATA[

    action = {
              "type": "ir.actions.act_window",
              "view_mode": "form",
              "res_model": 'x_variants_cost_wizard', #ATTENTION : CA DOIT ETRE UN TEXTE
              "target": 'new', #Pour que ce soit en POP UP
            }
    ]]>
            </field>
    </record>

**** Wizard Lines ****

#Logique : On ouvre un wizard qui est composé de lignes avec des caractéristiques pour chaque ligne, EXEMPLE : Wizard sur product.template qui affiche des lignes avec les product.product et leurs caractéristiques
#Procédure : Créer un modèle (TRANSIENT) wizard qui possède comme field des wizard_lines. Créer ensuite un modèle wizard_line qui contient les caractéristiques de l'objet qui nous intéresse

** 1 : wizard_line modèle **

#TRANSIENT

<odoo>
    <data noupdate="1">
        <record id="variants_cost_wizard_line_model" model="ir.model">
            <field name="name">Variants cost wizard lines</field>
            <field name="model">x_wizard_line</field>
            <field name="transient" eval="True"/>
        </record>
    </data>
</odoo>

** 1.1 : wizard_line field **

<odoo>
    <data noupdate="1">

        #Vu que le wizard sera un modèle avec un field one2many vers wizard_line, il faut un field many2one pour les relier (!Utiliser ce field donc le modèle du wizard)
        <record id="x_rel_wizard_line" model="ir.model.fields">
            <field name="name">x_rel_wizard_line</field>
            <field name="ttype">many2one</field>
            <field name="relation">x_variants_cost_wizard</field>
            <field name="model_id" ref="variants_cost_wizard_line_model"/>
            <field name="field_description">Wizard line link</field>
        </record>

        #Ici par exemple, chaque wizard_line sera liée à un product.product (variante)
        <record id="x_variant_field" model="ir.model.fields">
            <field name="name">x_variant_field</field>
            <field name="ttype">many2one</field>
            <field name="relation">product.product</field>
            <field name="model_id" ref="variants_cost_wizard_line_model"/>
            <field name="field_description">Variant</field>
        </record>

        <record id="x_supplier_field" model="ir.model.fields">
            <field name="name">x_supplier_field</field>
            <field name="ttype">many2one</field>
            <field name="relation">res.partner</field>
            <field name="model_id" ref="variants_cost_wizard_line_model"/>
            <field name="field_description">Supplier</field>
        </record>

    </data>
</odoo>

** 2 : Créer le modèle wizard **

#TRANSIENT

<odoo>
    <data noupdate="1">
        <record id="variants_cost_wizard_model" model="ir.model">
            <field name="name">Variants cost</field>
            <field name="model">x_variants_cost_wizard</field>
            <field name="transient" eval="True"/>
        </record>
    </data>
</odoo>

** 2.1 : Field du modèle wizard **

<odoo>
    <data noupdate="1">
        <record id="x_wizard_lines" model="ir.model.fields">
            <field name="name">x_wizard_lines</field>
            <field name="ttype">one2many</field>
            <field name="relation">x_wizard_line</field>
            <field name="model_id" ref="variants_cost_wizard_model"/>
            <field name="relation_field">x_rel_wizard_line</field> #Vers le field many2one du wizard_line
            <field name="field_description">Variant</field>
        </record>
    </data>
</odoo>

#Le modèle wizard est donc liée à un ensemble de wizard_line


** 3 : Mettre les wizard lines dans la vue du wizard **

    <record id="view_variants_cost_wizard_model" model="ir.ui.view">
        <field name="name">Add variants cost</field>
        <field name="model">x_variants_cost_wizard</field>
        <field name="arch" type="xml">
            <form>
                <group>
                    <field name="x_wizard_lines" nolabel="1">                   #Mettre le field x_wizard_lines qui représente le modèle wizard_line
                        <tree>                                                  #En mettant <tree> on entre dans le modèle wizard_line !!!!ATTENTION : Ne pas fermer la balise <field> et mettre le tree dedans
                            <field name="x_variant_field" string="Variant"/>    #Ici on met les champs de modèle wizard_line
                            <field name="x_supplier_field" string="Vendor"/>
                            <field name="x_cost_field" string="Cost"/>
                        </tree>
                    </field>
                </group>
                <footer>
                    <button name="%(variants_cost_wizard_action)d"  string="Add costs" type="action" class="btn-primary"/>
                    <button string="Cancel" class="btn-default" special="cancel"/>
                </footer>

            </form>
        </field>
    </record>

** 4 : Apparation wizard avec une action.server **

#on peut faire apparaitre le wizard avec une action.server liée à un bouton

* 4.1 : Déclarer la action.server *


    <record id="action_view_variants_cost_wizard_model" model="ir.actions.server"> #Nom du bouton
        <field name="name">Display wizrd</field>
        <field name="model_id" ref="product.model_product_template"/>
        <field name="state">code</field>
        <field name="sequence">20</field>
        <field name="code">
<![CDATA[

]]>
        </field>
    </record>

* 4.2 : Appeler le wizard *


<![CDATA[

action = {
          "type": "ir.actions.act_window",
          "view_mode": "form",
          "res_model": 'x_variants_cost_wizard',
          "target": 'new', #!!POP UP
        }
]]>
>

* 5 : Préremplir le wizard *

    <record id="action_view_variants_cost_wizard_model" model="ir.actions.server">
        <field name="name">Display wizrd</field>
        <field name="model_id" ref="product.model_product_template"/>
        <field name="state">code</field>
        <field name="sequence">20</field>
        <field name="code">
<![CDATA[
wiz_id = env['x_variants_cost_wizard'].create({                 #Création du wizard
    'x_wizard_lines': [(0, 0, {                                 #Comprehension list pour remplir le wizard (Remplir les x_wizard_lines)
            'x_variant_field': variant.id,
        }) for variant in record.product_variant_ids
                       ]
    })


#On met res_id avec l'id du wizard qu'on vient de créer
action = {
          "type": "ir.actions.act_window",
          "view_mode": "form",
          "res_model": 'x_variants_cost_wizard',
          "res_id": wiz_id.id,
          "target": 'new',
        }
]]>
        </field>
    </record>

** Option affichage pour <tree> **

<field name="x_wizard_lines" nolabel="1" >    #Nolabel pour ne pas afficher le titre
    <tree editable="bottom" create="0" delete="0    "> #"create" supprime le bouton "Add line" et delete retire la poubelle pour supprimer
        <field name="x_variant_field" string="Variant" readonly="1"/>
        <field name="x_supplier_field" string="Vendor"/>
        <field name="x_cost_field" string="Cost"/>
    </tree>
</field>


































product = env['product.template'].search([('id', '=', )])

for variant in product.product_variants_ids:
    wiz_line = env['x_wizard_line'].create({
            'x_rel_wizard_line':,
            'x_variant_field': variant,
        })

    wizard_lines |= wiz_line

ctx = {'x_wizard_lines': [(0, 0, wizard_lines)]}

action = {
          "type": "ir.actions.act_window",
          "view_mode": "form",
          "res_model": 'x_variants_cost_wizard',
          "context": ctx,
          "target": 'new',
        }