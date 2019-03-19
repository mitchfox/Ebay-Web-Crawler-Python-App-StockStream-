# -----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N9968296
#    Student name: MITCHELL FOX
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
# --------------------------------------------------------------------#


# -----Assignment Description-----------------------------------------#
#
#  Online Shopping Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
# --------------------------------------------------------------------#


# -----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.
#

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen
import webbrowser
import os


# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *
from functools import partial
from random import *


# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *


#
# --------------------------------------------------------------------#


# -----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it on a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url='http://www.wikipedia.org/',
             target_filename='download',
             filename_extension='html'):
    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding='UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents


#
# -----Student's Solution---------------------------------------------#
# Initialise Global Variables
global cart, total_cost_cart, total_cost, cart_floats, cart_size, cart_text, imgs_list, product_list
cart = []
total_cost_cart = []
total_cost = 0
cart_floats = []
cart_size = 0
cart_text = []
imgs_list = []
product_list = []


# Function for Finding Info Online
def extract_online_info():
    global desk_titles, desk_prices, desk_imgs
    # Open Url
    web_page = urlopen("https://www.ebay.com.au/b/Home-Office-Desks/88057/bn_1664690?LH_BIN=1&rt=nc")
    # Read + Decode the Html of the Doc
    web_page_contents = web_page.read().decode('UTF-8')
    # Reg Exp To Find Desk Titles
    desk_titles = findall('">([A-Za-z ]+)<\/h3>', web_page_contents)
    desk_titles = desk_titles[:10]
    # Reg Exp To Find Desk Prices
    desk_prices = findall('[^A-Z*]">AU\s\$([\d|\d*.d*]+)<', web_page_contents)
    desk_prices = desk_prices[:10]
    # Reg Exp To Find Desk Prices
    desk_imgs = findall('src="(http?s?:?\/\/[^"\']*\.(?:jpg))">', web_page_contents)
    desk_imgs = desk_imgs[:10]

    global monitor_titles, monitor_prices, monitor_imgs
    # Open Url + Read + Decode the Html of the Doc
    web_page = urlopen("https://www.ebay.com.au/b/Computer-Monitors/80053/bn_504066?LH_BIN=1&rt=nc")
    web_page_contents = web_page.read().decode('UTF-8')
    # Reg Exp To Find Monitor Titles
    monitor_titles = findall('">([A-Za-z\s\0-9\:]+)<\/h3>', web_page_contents)
    monitor_titles = monitor_titles[:10]
    # Reg Exp To Find Monitor Prices
    monitor_prices = findall('[^A-Z*]">AU\s\$([\d|\d*.d*]+)<', web_page_contents)
    monitor_prices = monitor_prices[:10]
    # Reg Exp To Find Monitor Imgs
    monitor_imgs = findall('src="(http?s?:?\/\/[^"\']*\.(?:jpg))">', web_page_contents)
    monitor_imgs = monitor_imgs[:10]


extract_online_info()


# Function for Finding Info in Downloaded Html Files
def extract_downloaded_info():
    global novelty_sock_titles, novelty_sock_prices, novelty_sock_imgs
    # Open + Read the Html of the Doc
    novelty_socks = open('noveltysocks.html', encoding='utf8')
    novelty_socks_html = novelty_socks.read()
    # Reg Exp To Find Sock Titles
    novelty_sock_titles = findall('">([A-Za-z -]+)</a>\s*</h3>', novelty_socks_html)
    novelty_sock_titles = novelty_sock_titles[:10]
    # Reg Exp To Find Sock Prices
    novelty_sock_prices = findall('"><b>AU \$</b>([\d|\d*.d*]+)', novelty_socks_html)
    novelty_sock_prices = novelty_sock_prices[:10]
    # Reg Exp To Find Sock Images
    novelty_sock_imgs = findall('imgurl="(https?:\/\/.*\.(?:png|jpg))', novelty_socks_html)
    novelty_sock_imgs = novelty_sock_imgs[:10]
    novelty_socks.close()

    # TVs
    global tv_titles, tv_prices, tv_imgs
    tv = open('televisions.html', encoding='utf8')
    tv_html = tv.read()
    # Reg Exp To Find Tv Titles
    tv_titles = findall('>([A-Za-z\s\-\.\!\=\w\"\'\0-9]+)<\/h3></a>', tv_html)
    tv_titles = tv_titles[:10]
    # Reg Exp To Find Tv Prices
    tv_prices = findall('">([AU $\d|AU $\d*.d*]+)<\/span></div>', tv_html)
    tv_prices = tv_prices[:10]
    # Reg Exp To Find Tv Images
    tv_imgs = findall('data-src="(http?s?:?\/\/[^"\']*\.(?:jpg))">', tv_html)
    tv_imgs = tv_imgs[:10]
    tv.close()


extract_downloaded_info()


# CREATING APP  GUI - # Create Window & Initialise
root = Tk()
root.title("Stock Stream Shopping Web App")
root.minsize(width=400, height=400)
root.maxsize(width=400, height=400)

# TODO - Make the Logo Clear and not Pixelated
logo = PhotoImage(file="stock_stream_logo.gif")
logoplacement = Label(image=logo, pady=15, padx=10)
logoplacement.place(x=50, y=25)

# Creating the Frame / Grid
maingrid = Frame(root)
maingrid.grid(column=0, row=0, sticky=(N, W, E, S))
maingrid.pack(pady=(130, 20), padx=10)


# Novelty Socks Popup
def popup_one(button1):
    # Initialising First Window
    new_window1 = Toplevel(root)
    new_window1.title("Stock Stream Discount Novelty Socks")
    new_window1.minsize(width=300, height=500)
    titles_prices1 = []
    index = -1

    # Function to append
    def add_to_cart1(index):
        # When Button Pressed, Append relevant Label Data
        add_button.config(cart.append(titles_prices1[index][0]))

    # Produce 10 Labels & Add To Cart Buttons and Connect to Relevant Label through Partial
    for i in range(10):
        item_title1 = Label(new_window1, wraplengt=250, padx=2, pady=2, text="#" + str(i + 1) + " " +
                                                                             novelty_sock_titles[i]\
        + " - $" + novelty_sock_prices[i])
        item_title1.grid(row=i, column=1)

        add_button = Button(new_window1, height=3, command=partial(add_to_cart1, i), padx=2, pady=2, width=10,
                            text="Add To Cart")
        add_button.grid(row=i, column=2)
        # Append Both to List
        titles_prices1.append((novelty_sock_titles[i] + " - $" + novelty_sock_prices[i] + "   "
                               + novelty_sock_imgs[i], add_button))


# Tv's Popup
def popup_two(button2):
    # Initialising Second Window
    new_window2 = Toplevel(root)
    new_window2.title("Stock Stream Discount TVs")
    new_window2.minsize(width=300, height=500)
    titles_prices2 = []
    index = -1

    # Function to append
    def add_to_cart2(index):
        # When Button Pressed, Print relevant Label Data
        add_button.config(cart.append(titles_prices2[index][0]))

    # Produce 10 Labels & Add To Cart Buttons and Connect to Relevant Label through Partial
    for i in range(10):
        item_title2 = Label(new_window2, wraplengt=250, padx=2, pady=2, text="#" + str(i + 1) + " " + tv_titles[i]
                                                                             + " - $" + tv_prices[i])
        item_title2.grid(row=i, column=1)
        add_button = Button(new_window2, height=3, command=partial(add_to_cart2, i), padx=2, pady=2, width=10,
                            text="Add To Cart")
        add_button.grid(row=i, column=2)
        # Append Both to List
        titles_prices2.append((tv_titles[i] + " - $" + tv_prices[i] + "   " + tv_imgs[i], add_button))


def popup_three(button3):
    # Initialising Third Window
    new_window3 = Toplevel(root)
    new_window3.title("Stock Stream Discount Desks")
    new_window3.minsize(width=300, height=500)
    titles_prices3 = []
    index = -1

    # Function to append
    def add_to_cart3(index):
        # When Button Pressed, Print relevant Label Data
        add_button.config(cart.append(titles_prices3[index][0]))

    for i in range(10):
        # Produce 10 Labels & Add To Cart Buttons and Connect to Relevant Label through Partial
        item_title2 = Label(new_window3, wraplengt=250, padx=2, pady=2, text="#" + str(i + 1) + " " + desk_titles[i]
                                                                             + " - $" + desk_prices[i])
        item_title2.grid(row=i, column=1)
        add_button = Button(new_window3, height=3, command=partial(add_to_cart3, i), padx=2, pady=2, width=10,
                            text="Add To Cart")
        add_button.grid(row=i, column=2)
        # Append Both to List
        titles_prices3.append((desk_titles[i] + " - $" + desk_prices[i] + "   " + desk_imgs[i], add_button))


def popup_four(button4):
    # Initialising Fourth Window
    new_window4 = Toplevel(root)
    new_window4.title("Stock Stream Discount Monitors")
    new_window4.minsize(width=300, height=500)
    titles_prices4 = []
    index = -1

    # Function to append
    def add_to_cart4(index):

        # When Button Pressed, Print relevant Label Data
        add_button.config(cart.append(titles_prices4[index][0]))

    for i in range(10):
        # Produce 10 Labels & Add To Cart Buttons and Connect to Relevant Label through Partial
        item_title4 = Label(new_window4, wraplengt=250, padx=2, pady=2, text="#" + str(i + 1) + " " +
                                                                        monitor_titles[i] + " - $" + monitor_prices[i])
        item_title4.grid(row=i, column=1)
        # Produce Add To Cart Buttons and Connect to Relevant Label through Partial
        add_button = Button(new_window4, height=3, command=partial(add_to_cart4, i), padx=2, pady=2, width=10,
                            text="Add To Cart")
        add_button.grid(row=i, column=2)
        # Append Both to List
        titles_prices4.append((monitor_titles[i] + " - $" + monitor_prices[i] + "   " + monitor_imgs[i], add_button))


# About Us PopUp
def about_us():
    about_us_window = Toplevel(root)
    about_us_window.title("Stock Stream | About Us")
    about_us_window.minsize(width=250, height=200)
    about_us_label = Label(about_us_window, wraplengt=200, padx=5, pady=5,
                       text="ABOUT US")
    about_us_label.grid(row=0, column=0)
    about_us_description = Label(about_us_window, wraplengt=250, padx=5, pady=10,
                                 text="Stock Stream is a place where opening a browser is not required to purchase the "
                                 "latest deals or products added to the web. Updated weekly, the stock stream app "
                                 "allows your to browse with ease.")
    about_us_description.grid(row=1, column=0)

    # Insert References into About Us Window
    reference_label1 = Label(about_us_window, wraplengt=250, padx=2, pady=10,
                             text="NOVELTY SOCKS - https://www.ebay.com/bhp/novelty-socks")
    reference_label1.grid(row=2, column=0)
    reference_label2 = Label(about_us_window, wraplengt=250, padx=2, pady=10,
                             text="TVS - https: // www.ebay.com / sch / i.html?_from = R40 & _nkw = tvs & _"
                                  "sacat = 0 & LH_BIN = 1")
    reference_label2.grid(row=3, column=0)
    reference_label3 = Label(about_us_window, wraplengt=250, padx=2, pady=10, font=(10),
                             text="DESKS - https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=p2334524.m570."
                                  "l2632.R3.TR12.TRC2.A0.H0.Xdesks.TRS0&_nkw=desks&_sacat=11828&LH_TitleDesc=0&_os"
                                  "acat=3197&_odkw=computer+desks&LH_BIN=1&LH_TitleDesc=0")
    reference_label3.grid(row=4, column=0)
    reference_label4 = Label(about_us_window, wraplengt=250, padx=2, pady=10,
                             text="MONITORS - https: // www.ebay.com.au / b / Computer - Monitors "
                                  "/ 80053 / bn_504066?LH_BIN = 1 & rt = nc")
    reference_label4.grid(row=5, column=0)


# The View Cart Pop Up Window
def view_cart_popup():
    view_cart_window = Toplevel(root)
    view_cart_window.minsize(width=250, height=200)
    view_cart_window.title("Stock Stream - View Cart")
    global cart_size
    cart_size = len(cart)

    # Clear Cart
    def clear_cart():
        cart.clear()
        view_cart_window.destroy()

    # Close Empty Cart
    def close_empty_cart():
        view_cart_window.destroy()

    # Determine if Cart is Empty
    if cart_size == 0:
        empty_cart = Label(view_cart_window, wraplengt=200, padx=50, pady=100, text="You have an Empty " \
                                                                                    "Cart! Happy Shopping :)")
        empty_cart.grid(row=0, column=0)

        return_home = Button(view_cart_window, pady=40, text="Back to Shop", command=close_empty_cart)
        return_home.grid(row=1, column=0)

    else:
        # Print Each Item in Cart to View Cart Window & Remove Image Url that is attached within List
        for item in range(cart_size):
            # Redefines text as everything up until '3' spaces to remove unecessary Url from Cart Page
            cart_text = cart[item].partition("   ")[0]
            display_cart_item = Label(view_cart_window, pady=10, padx=10, wraplengt=250, text="1 x " + cart_text)
            display_cart_item.grid(row=item, column=0)

        # Find Numbers in Product Cart using Reg Ex, Convert to Floats,  Total
        def dividing_cart():
            # Make Cart one String
            cart_string = ''.join(cart)
            # Find all Prices of Cart
            cart_cost = findall('\$([\d|\d*\.\d*]+)\s', cart_string)
            # Make each item String a Float
            for item in cart_cost:
                cart_floats.append(float(item))
            global total_cost
            # Sum all Float Items in Cart
            total_cost = (sum(cart_floats))
            total_cost = round(total_cost, 1)

        dividing_cart()

        # Print Total Cost
        total_cost_label = Label(view_cart_window, pady=10, text="Total Cost of all Items = $" + str(total_cost))
        total_cost_label.grid(row=item+1, column=0)
        # Finished Shopping / Print Invoice Button
        invoice_button1 = Button(view_cart_window, pady=10, text="Finished Shopping? Print Invoice",
                                 command=new_invoice)
        invoice_button1.grid(row=item+2, column=0)
        # Add command function to Clear Cart (Remove all items from a list)
        clear_cart_button = Button(view_cart_window, pady=10, text="Clear Cart & Return", command=clear_cart)
        clear_cart_button.grid(row=item+3, column=0)


# Function to Create an Invoice (New)
def new_invoice():
    # Generate Random Invoice Number between 1001 & 1999
    invoice_number = randint(1001, 9999)
    invoice = open('invoice.html', 'w')
    # Html with CSS Styling
    invoice_html = '<!DOCTYPE html>\n<html lang="en"\n<head>\n<meta charset="UTF-8">\n<title>' \
                   'Stock Stream</title>\n</head>'
    invoice_html += '\n<body style="text-align:center;">\n<img style="display: block; margin-left: auto; ' \
                    'margin-right: auto; padding-top: 40px; width: 20%" src="stock_stream_logo_HD.png">'
    invoice_html += '\n<h1 style="font-family: Helvetica; font-size: 24px; text-align:center; ' \
                    'padding-top: 40px;">Your Stock Stream Purchase Invoice : ' + str(invoice_number) + '</h1>'

    # Print Cart Items to Invoice
    for i in range(cart_size):
        # Partition to separate List Items and insert the URL and Title / Price separately
        product_list.append(cart[i].partition(" -")[0])
        invoice_html += '<div style="height: 300px; width: 60%; display: inline-block; margin-left: auto; ' \
                        'margin-right: auto; margin-top: 40px; background-color: #f7f7f7; padding: 20px">' \
                        '<img style="display: block; margin-left: auto; ' \
                        'margin-right: auto;" src="' + cart[i].partition("   ")[-1] + '"' \
                        'alt="Product Images"><ul style="font-family: Helvetica; font-size: 18px; text-align:center; ' \
                        'padding-top: 20px;">' + "Item " + str(i+1) + ": " + cart[i].partition("   ")[0] + '</ul></div>'
        invoice_html += '<br></br>'

    invoice_html += '<h1 style="font-family: Helvetica; font-size: 24px; text-align:center; padding-top: ' \
                    '40px; padding-bottom: 40px;">Cart Sub Total - $' + str(total_cost) + '</h1>'
    invoice_html += '<ul><li style="list-style-type: none;"><a href="https://www.ebay.com/bhp/' \
                    'novelty-socks">Novelty Sock Reference</a></li><li style="list-style-type: none;"><a ' \
                    'href="https:// www.ebay.com / sch / i.html?_from = R40 & _nkw = tvs & _"sacat = 0 ' \
                    '& LH_BIN = 1">Tv Reference</a></li><li style="list-style-type: none;"><a href="https:' \
                    '//www.ebay.com.au/sch/i.html?_from=R40&_trksid=p2334524.m570.' \
                    'l2632.R3.TR12.TRC2.A0.H0.Xdesks.TRS0&_nkw=desks&_sacat=11828&LH_TitleDesc=0&_osacat=3197&_' \
                    'odkw=computer+desks&LH_BIN=1&LH_TitleDesc=0">Desk References</a></li>' \
                    '<li style="list-style-type: none;"><a href="https: // ' \
                    'www.ebay.com.au / b / Computer - Monitors / 80053 / bn_504066?LH_BIN = 1 & rt = nc"' \
                    '>Monitor Reference</a></li></ul>'
    invoice_html += '\n</body>\n</html>'
    invoice.write(invoice_html)
    invoice.close()
    webbrowser.open('file://' + os.path.realpath('invoice.html'))

    # PART B - Insert Purchases into ShoppingCart Table
    def insert_data(names, prices):
        # Connect to Database
        conn = connect(database='shopping_cart.db')
        # Get a cursor on the database
        c = conn.cursor()
        # To Execute each item to SQL Table, name of product and price
        for i in range(len(cart)):
            c.execute('INSERT INTO ShoppingCart (Item, Price) VALUES (?, ?)', (names[i], prices[i]))

        conn.commit()

    insert_data(product_list, cart_floats)


# View Cart Button
view_cart_button = Button(maingrid, pady=10, text="View Cart", command=view_cart_popup)
view_cart_button.grid(row=4, column=1)
# Invoice Button to Open File in Browser
about_button = Button(maingrid, pady=10, text="About Us", command=about_us)
about_button.grid(row=4, column=0)

# Create & Position Labels, Call Popup Function on Label Click
products_one = Label(maingrid, width=16, wraplengt=120, height=5, bg="LightSkyBlue", text="CLEARANCE NOVELTY SOCKS")
products_one.grid(row=1, column=0, padx=10, pady=10)
products_one.bind("<Button>", popup_one)
products_two = Label(maingrid, width=16, wraplengt=120, height=5, bg="LightSkyBlue", text="CLEARANCE TVs")
products_two.grid(row=1, column=1, padx=10, pady=10)
products_two.bind("<Button>", popup_two)
products_three = Label(maingrid, width=16, wraplengt=120, height=5, bg="DeepSkyBlue", text="NEW DESKS")
products_three.grid(row=2, column=0, padx=10, pady=10)
products_three.bind("<Button>", popup_three)
products_four = Label(maingrid, wraplengt=120, width=16, height=5, bg="DeepSkyBlue", text="NEW MONITORS")
products_four.grid(row=2, column=1, padx=10, pady=10)
products_four.bind("<Button>", popup_four)

# Run Main Function
root.mainloop()
