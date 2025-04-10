# Initially all jsons in the correct format

def make_returned(book: dict):
    # translate count_pages to pages
    formatted_book = book.copy()
    formatted_book['pages'] = formatted_book['count_pages']
    formatted_book.pop('count_pages')
    return formatted_book

seller1 = {
    "first_name": "Bob",
    "last_name": "Johnson",
    "e_mail": "bobjohnson@gmail.com",
    "password": "Apple1_2"
}
seller2 = {
    "first_name": "Steve",
    "last_name": "Jobs",
    "e_mail": "stevejobs@gmail.com",
    "password": "Elephant1_2"
}

book1 = {
        "title": "Clean Architecture",
        "author": "Robert Martin",
        "count_pages": 300,
        "year": 2025,
        "seller_id": 1 # can be changed
}
book2 = {
        "title": "Eugeny Onegin",
        "author": "Pushkin",
        "year": 2022,
        "count_pages": 104,
        "seller_id": 1 # can be changed
}
book3 = {
        "title": "Mziri",
        "author": "Lermontov",
        "year": 2022,
        "count_pages": 104,
        "seller_id": 1 # can be changed
}