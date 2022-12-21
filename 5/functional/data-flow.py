import csv


class DataFlow:
    def __init__(self):
        self.data = []

    def read(self, file):
        df = DataFlow()
        with open(file, 'r') as f:
            reader = csv.reader(f)
            df.data = [tuple(row) for row in reader][1:]
        return df

    def write(self, file):
        with open(file, 'w') as f:
            writer = csv.writer(f)
            for row in self.data:
                writer.writerow(row)

    def filter(self, function):
        df = DataFlow()
        df.data = [t for t in self.data if function(t)]
        return df

    def map(self, function):
        df = DataFlow()
        df.data = [function(t) for t in self.data]
        return df

    def flatmap(self, function):
        df = DataFlow()
        result = []
        for t in self.data:
            result.extend(function(t))
        df.data = result
        return df

    def group(self, function):
        df = DataFlow()
        groups = {}
        for t in self.data:
            key = function(t)
            if key in groups:
                groups[key].append(t)
            else:
                groups[key] = [t]
        df.data = [(k, v) for k, v in groups.items()]
        return df

    def reduce(self, function):
        df = DataFlow()
        if not self.data or not isinstance(self.data[0], tuple):
            df.data = function(self.data)
        else:
            result = []
            for key, value in self.data:
                result.append((key, function(value)))
            df.data = result
        return df

    def join(self, y, function):
        df = DataFlow()
        result = []
        for t1 in self.data:
            for t2 in y.data:
                result.append(function(t1, t2))
        df.data = result
        return df

    def __str__(self):
        return str(self.data)


if __name__ == "__main__":
    dataflow = DataFlow()
    d = dataflow.read("file.csv")
    flat = d.map(lambda t: (t[0], eval(t[3])))
    bd = flat.filter(lambda t: "HPDA" in t[1])
    bd.write("out.csv")
    fm = flat.flatmap(lambda t: [[t[0], x]
                      for x in t[1]])
    z = fm.group(lambda t: t[1])
    r = z.reduce(lambda tl: len(tl))
    print(r)

    def joinFunc(x, y):
        if x != y:
            return [x, y]
        else:
            return None
    e = fm.join(fm, joinFunc)
    print(e)
