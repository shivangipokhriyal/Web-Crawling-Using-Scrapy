# Web-Crawling-using-Scrapy

This is the project where I have scraped the website 'Books to Scrape' and scraped all the book title, their urls, and price.
The output is store in a csv file BookCrawler.csv.
/* Sort the dataset by elig_csi, UW_year, and year in descending order */
proc sort data=your_dataset;
  by elig_csi UW_year year descending;
run;

/* Create a new dataset to store the transformed data */
data transformed_dataset(keep=elig_csi UW_year year Count_Accepted Count_Inprogress Count_Quoted);
  set your_dataset;
  by elig_csi UW_year;

  /* Initialize variables to store the latest year and the corresponding counts */
  retain retained_year retained_accepted retained_inprogress retained_quoted .;

  /* If Count_Accepted is 1, use that year */
  if Count_Accepted = 1 then do;
    retained_year = year;
    retained_accepted = Count_Accepted;
    retained_inprogress = Count_Inprogress;
    retained_quoted = Count_Quoted;
  end;

  /* If Count_Accepted is 0 and Count_InProgress is 1, and retained_year is not yet assigned, use that year */
  else if Count_Accepted = 0 and Count_Inprogress = 1 and retained_year = . then do;
    retained_year = year;
    retained_accepted = Count_Accepted;
    retained_inprogress = Count_Inprogress;
    retained_quoted = Count_Quoted;
  end;

  /* If Count_Accepted, Count_InProgress are both 0 and Count_Quoted is 1, and retained_year is not yet assigned, use that year */
  else if Count_Accepted = 0 and Count_Inprogress = 0 and Count_Quoted = 1 and retained_year = . then do;
    retained_year = year;
    retained_accepted = Count_Accepted;
    retained_inprogress = Count_Inprogress;
    retained_quoted = Count_Quoted;
  end;

  /* If no condition met yet and year is later than the retained year, update retained_year and counts */
  else if year > retained_year then do;
    retained_year = year;
    retained_accepted = Count_Accepted;
    retained_inprogress = Count_Inprogress;
    retained_quoted = Count_Quoted;
  end;

  /* Output the transformed data */
  if last.UW_year then do;
    elig_csi = first.elig_csi;
    output;
  end;
run;

/* Display the transformed dataset */
proc print data=transformed_dataset noobs;
run;
