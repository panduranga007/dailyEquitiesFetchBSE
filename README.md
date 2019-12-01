# Daily Equities Fetch BSE
- A script downloads the equities file(bhavcopy) for a given date and pushes the details to a redis server
- A  CherryPy Applcation that has two services
  - To search with given companyname(SC_NAME)
  - To fetch top 10/20/50/100 equities in each category of High/Low/Open/Close
