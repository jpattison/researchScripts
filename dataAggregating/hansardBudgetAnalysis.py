import hansardHandler
import cosineComparison
import graphs


def cosineHansard(dataset, queryTranscript, queryName, reference, k):
    matrix, query = cosineComparison.calculateComparison(dataset, queryTranscript, k)
    scores = cosineComparison.scoreDocuments(query, matrix, reference)

    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "Hansard Cosine. Reference = {0} K = {1}".\
        format(queryName,k), values)


queryTranscript, dataset, reference = \
    hansardHandler.getHansardBudgets(2005, 2017, 2015)

cosineHansard(dataset, queryTranscript, "2015", reference, 1000)

