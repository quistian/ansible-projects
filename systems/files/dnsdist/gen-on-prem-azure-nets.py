#!/usr/bin/env python3

from bs4 import BeautifulSoup


html_input_file = "dcb-ccg.html"

def main():
    in_section = False
    print('generate networks file for Azure DNS forwarding')
    with open(html_input_file) as fd:
        soup = BeautifulSoup(fd, "html.parser")
#       print(soup.prettify())
#       print(soup.get_text())
#       exit()
        for td in soup.find_all('td'):
            if td.string is not None:
                print(td.strings)
                vals = td.string.split('<br>')
                print(vals)
                for val in vals:
                    if 'dcb-ccg-td' in val:
                        in_section = True
                    elif 'outside' in val:
                        in_section = False
                    prefix = val[:5]
                    if in_section and prefix in ['128.1', '142.1', '10.19']:
                        print(val)


if __name__ == '__main__':
    main()
