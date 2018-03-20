from bs4 import BeautifulSoup
import requests

fh = open("table_44.html", "r")
bs = BeautifulSoup(fh, "lxml")

# url = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-18-000007&xbrl_type=v#'
# url = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-18-000007&xbrl_type=v#'
# url = 'https://www.sec.gov/Archives/edgar/data/320193/000032019318000007/a10-qq1201812302017.htm'
# r = requests.get(url)
# x = BeautifulSoup(r.text, "lxml")
# a = x.html.body.find_all('table')
# print(x)

# i = 0
# for b in a:
#     # print(type(b.text))
#     filename = "table_{}.html".format(i)
#     print(filename)
#     fh = open("table_{}.html".format(i), 'w')
#     # print(str(b))
#     fh.write(str(b))
#     fh.close()
#     # break
#     i = i + 1

def generate_dict(table):
    results = []
    header = []
    # for row in table.findAll('tr'):
    #     aux = row.findAll('th')
    #     print(len(aux))
    #     if not len(aux):
    #         continue
    #     # for a in aux:
    #     #     print(a.string)
    #     alist = [a.string for a in aux]
    #     print(alist)
    #     if alist:
    #         header = alist
    #
    # print(header)

    for row in table.findAll('tr'):
        bux = row.findAll('td')
        blist = [b.string for b in bux]
        obj = {}
        for index, val in enumerate(blist):
            if val:
                print("(", index, ")", val, end=" ")
            # obj[header[index]] = val
        # print(obj)
        print()
        if obj:
            results.append(obj)

    return results

print(generate_dict(bs))
