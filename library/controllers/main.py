from odoo import http

class Books(http.Controller):

    @http.route('/library/books', auth='user', website=True)
    def list(self, **kwargs):
        Book = http.request.env['product.product']
        books = Book.search([('is_book','=',True)])
        return http.request.render('library.book_list_template', {'books': books})

    @http.route('/library/book/<model("product.product"):book>', auth='user', website=True)
    def book(self, book, **kwargs):
        
        book.is_rented = True
        return http.request.redirect('/library/books')