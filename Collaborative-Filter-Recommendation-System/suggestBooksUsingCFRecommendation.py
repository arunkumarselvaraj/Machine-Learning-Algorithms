import sys
import pandas
import numpy
import math

def Suggestbooks(userReadRatedList):
    userRatingData = pandas.read_csv("dataset/ratings.csv")
    userRatingData = userRatingData[['userid', 'bookid', 'rating']]

    #selecting only 5 star rated data
    userRatingData = userRatingData[userRatingData['rating'] > 4]
    fiveStarBookList = userRatingData['bookid'].tolist();
    userPreferenceFiveStarRatedBooks = list(set(userReadRatedList) & set(fiveStarBookList))

    #select books that user rated 5 stars and other users who have read those books
    userBookOtherUsersData = userRatingData[userRatingData['bookid'].isin(userReadRatedList)]
    userBookOtherUsersMatrix = userBookOtherUsersData.pivot_table(index='userid', columns='bookid', values='rating', fill_value=0)
    userBookData = pandas.DataFrame({'userid': 0, 'bookid': userPreferenceFiveStarRatedBooks, 'rating': 5})
    userBookData = userBookData[['userid', 'bookid', 'rating']].drop_duplicates(subset=['userid', 'bookid'])
    userBookMatrix = userBookData.pivot_table(index='userid', columns='bookid', values='rating', fill_value=0)

    #finding user and other users similarity matrix
    userOtherUsersSimilarityMatrix = numpy.matmul(userBookMatrix, userBookOtherUsersMatrix.transpose());
    otherUsersSortedList = sorted(numpy.unique(userRatingData['userid'].tolist()))
    userOtherUsersSimilarityValues = []
    for i in range(0, len(userOtherUsersSimilarityMatrix[0])):
        userOtherUsersSimilarityValues.append([otherUsersSortedList[i], userOtherUsersSimilarityMatrix[0][i]])
    userOtherUsersSortedSimilarityValues = sorted(userOtherUsersSimilarityValues, key=lambda x: x[1], reverse=True)

    #finding books that user's similar have read but not the user, only top 100 books
    similarUsersBookList = []
    userUnreadSimilarUsersBookList = []
    for i in range(0, len(userOtherUsersSortedSimilarityValues)):
        if(userOtherUsersSortedSimilarityValues[i][1] > 0):
            particularSimilarUserBookList = userRatingData[userRatingData['userid'] == userOtherUsersSortedSimilarityValues[i][0]]['bookid'].tolist()
            similarUsersBookList.extend(particularSimilarUserBookList)
            userUnreadSimilarUsersBookListTop100 = set(similarUsersBookList).difference(userReadRatedList)
            if(len(userUnreadSimilarUsersBookListTop100) > 100):
                break;

    #printing result
    booksDetails = pandas.read_csv("dataset/books.csv")
    print("\nUser have read {0}".format(booksDetails[booksDetails['book_id'].isin(userReadRatedList)]['original_title'].tolist()))
    print("\nUser might like to read {0}".format(booksDetails[booksDetails['book_id'].isin(userUnreadSimilarUsersBookListTop100)]['original_title'].tolist()))

def main():
	userReadBooksID = [11870085, 5907, 5107, 2956, 24178, 1618, 22557272, 119322]
	Suggestbooks(userReadBooksID)

main()
