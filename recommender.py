from flask import Flask
from requests import get
from json import loads

app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
  return 'Navigate to: /isbn/YYYY/MM/DD/ to get a book recommendation!'

@app.route('/isbn/<int:year>/<int:month>/<int:day>/')
def isbn(year, month, day):
  pi_start = year + month + day
  max_range = 100
  try:
    pi_url = "http://pidigitsapi.com/api?startdigit=" + str(pi_start) + "&enddigit=" + str(pi_start + 6 + max_range)
    isbn_seed = str(loads(get(pi_url).text)["output"]["digits"])
  except:
    return "Failed to get digits of pi!"

  for i in range (max_range):
    isbn_val = isbn_seed[i:i+6+1]
    isbn_val = "97809" + isbn_val

    check_digit = 0
    check_sum = 0
    for i, digit in enumerate(isbn_val):
      if i % 2 == 0:
        check_sum_mult = 1
      else:
        check_sum_mult = 3

      check_sum += check_sum_mult * int(digit)

    check_digit = str((10 - (check_sum % 10) ) % 10)

    isbn_val += check_digit

    try:
      isbn_url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn_val
      book_data = loads(get(isbn_url).text)
    except:
      pass

    try:
      if int(book_data["totalItems"]) > 0:
        for book_datum in book_data["items"]:
          return "You should read: " + book_datum["title"] + " by " + book_datum["authors"][0] + " (and possibly other authors)"
    except:
      pass

  return "Couldn't find any books using ISBN: " + isbn_val
