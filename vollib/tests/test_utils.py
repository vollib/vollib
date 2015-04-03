from collections import OrderedDict
import simplejson as json
import pandas



def almost_equal(a,b,epsilon = 1.0e-7):
    return abs(a-b)< epsilon


class TestDataIterator(object):

    """
    >>> data_iterator = TestDataIterator()
    >>> print data_iterator.has_next()
    True
    >>> r = data_iterator.next_row()
    >>> print r['S']
    100.0
    """
    
    def __init__(self):
        self.data = json.load(open('test_data.json','rb'))
        columns = self.data['columns']
        grid_data = OrderedDict()

        for header in columns:
            grid_data[header]=[]

        for col in self.data['data']:
            for i in range(len(columns)):
                grid_data[columns[i]].append(col[i])

        self.df = pandas.DataFrame(grid_data)
        self.row_id = 0
        self.row_count = self.df.S.count()

    def next_row(self):
        if self.has_next():
            row = self.df.ix[self.row_id].to_dict()
            self.row_id +=1
            return row

    def has_next(self):
        return self.row_id < self.row_count
    
    
# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"