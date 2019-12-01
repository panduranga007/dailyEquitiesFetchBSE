# Daily Equities Fetch BSE
- A script that downloads the equities file(bhavcopy) for a given date and pushes the details to a redis server
- A  CherryPy Application that has two services
  - To search with given companyname(SC_NAME)
  - To fetch top 10/20/50/100 equities in each category of High/Low/Open/Close

A Small UI is made to show the form and tabulate the results.
