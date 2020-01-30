import os
from selenium import webdriver
import pandas as pd
driver = webdriver.Chrome(r"C:\Users\jyong\Desktop\chromedriver.exe") # use different browser if you want

player = "ABALDE, ALBERTO"
letter = player[0]

driver.get("https://www.euroleague.net/competition/players?letter=" + letter)


link = driver.find_element_by_xpath("//a[contains(text(), '" + str(player) + "')]").get_attribute("href") # instead of clicking the link...
driver.get(link) # ...visit it. This fixes that cookies popup error

headings = [] # array of headings

heading_row = driver.find_element_by_css_selector('#careerstats .PlayerGridHeader:first-of-type') # returns heading row of the first table in career stats
headings_objects = heading_row.find_elements_by_tag_name('th') # returns array of each column in that heading row

for heading in headings_objects: # for each of that heading column...
    headings.append(heading.get_attribute('innerText')) # ...append text values of those headings to headings array


rows = [] # all rows that have array of columns inside (two dimensional array) => [["td1", "td2"], ["td1", "td2"], ["td1", "td2"]]

just_rows = driver.find_elements_by_css_selector('#careerstats [class="PlayerGridRow"]') # returns every table row in careerstats tab with one and only class "PlayerGridRow"
for just_row in just_rows:
    columns = just_row.find_elements_by_tag_name("td") # returns every td (column) from each of these rows

    if len(columns) == len(headings): # if number of values is equal to number of headings
        row = [] # one row, which will have array of columns inside
        for column in columns: # for each of those columns...
            row.append(column.get_attribute('innerText').strip()) # append text content of those columns to that one row

        rows.append(row) # append that one row to array of rows


# almost the same thing as above, but this time this gets data from "Other Competition" table (which doesnt have same class names)
just_rows = driver.find_elements_by_css_selector('#careerstats .FieldValue table tr:not(:first-of-type)') # every row (except the first one) inside careerstats tab and inside .FieldValue
for just_row in just_rows:
    columns = just_row.find_elements_by_tag_name("td")

    if len(columns) == len(headings): # if number of values is equal to number of headings
        row = []
        for column in columns:
            row.append(column.get_attribute('innerText').strip())

        rows.append(row)


driver.quit() # just quits the browser window

result = pd.concat([pd.DataFrame(rows[i]) for i in range (len(rows))], ignore_index=True)

#convert the pandas dataframe to JSON
json_records = result.to_json(orient='records')

#pretty print to CLI with tabulate
#converts to an ascii table
print(result)

#get current working directory
path = os.getcwd()

#open, write, and close the file
f = open(path + "\\fhsu_payroll_data.json","w") #FHSU
f.write(json_records)
f.close()