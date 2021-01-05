# Predicting Global Box Office Revenue for Japanese and American Animated Films

For my [Metis](https://www.thisismetis.com/data-science-bootcamps) regression project, I built two separate linear regression models to predict global box office revenue for American and Japanese animated films, respectively.

## Table of Contents

* [Lessons Learned](#lessons-learned)
* [Visualizations](#visualizations)
* [Technologies](#technologies)
* [Metis](#metis)

## Lessons Learned

My American regression model performed okay with a test R-squared of .66, but my Japan model was a failure with a test R-squared of almost zero. This project taught me a number of lessons, which have helped me improve my subsequent Metis projects. 

1. Think carefully about what data I need to scrape beforehand since re-scraping data is time-expensive.
2. Do residual analysis throughout the modeling process, not at the very end.
3. Find additional/better data sources if the data source I’m working with is inadequate.
4. Give myself enough time to work on my PowerPoint presentation and be deliberate in the design, data visualizations, and storytelling.

## Visualizations

![japan movies largest residuals](https://user-images.githubusercontent.com/62628676/102674735-ff424400-4164-11eb-84fd-33e0c2fd2151.png)
![u.s. movies largest residuals](https://user-images.githubusercontent.com/62628676/102674724-f5204580-4164-11eb-8fbe-c3db6b5fd95e.png)

## Technologies

* Python 3.8
* BeautifulSoup 4.9.1
* Scikit-learn 0.23.1
* Pandas 1.0.5
* Numpy 1.18.5
* Seaborn 0.10.1

## Metis

[Metis](https://www.thisismetis.com/data-science-bootcamps) is a 12-week accredited data science bootcamp where students build a 5-project portfolio. 


