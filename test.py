import vektor as v

test1 = "I! don't like to playing around... I prefer to lay and lay and lay around!!"
test2 = "I.... dont like to lay around and lay around and lay around,,, I want to play and play and play around"

arrkalimat = [v.stem(test1), v.stem(test2)]
print("arrkalimat: ", arrkalimat)

print(v.setkata(arrkalimat))
matrix = v.wordcount_matx(arrkalimat)

test1v = matrix[0]
print(v.tf(test1v))

# df = v.pd.DataFrame(matrix)
# print(df)

print(v.idfvect(matrix))