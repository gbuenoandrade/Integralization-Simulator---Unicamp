import numpy as np
import matplotlib.pyplot as plt

class Course:
	def __init__(self):
		self.name = ''
		self.type = ''
		self.credits = 0
		self.grade = 0.0
		self.sem = ''

	def __str__(self):
		return self.name + ' ' + self.type + ' ' + str(self.credits) + ' ' + str(self.grade)

def parseFromFile(fname):
	def parseRevClass(v):
		c = Course()
		c.name = v.pop()
		if len(c.name) == 1:
			c.name += ' ' + v.pop()
		crd = v.pop()
		if len(crd) == 1:
			crd = v.pop()
		c.credits = int(crd)
		c.type = v.pop()
		if len(c.type) != 1:	#it doesn't count
			for i in range(3):
				v.pop()
			if len(v) != 0:
				return parseRevClass(v)
			else:
				return []
		try:
			grd = list(v.pop())
			for i in range(len(grd)):
				if grd[i] == ',':
					grd[i] = '.'
					break
			grd = ''.join(grd)
			c.grade = float(grd)
		except ValueError:
			for i in range(3):
				v.pop()
			if len(v) != 0:
				return parseRevClass(v)
			else:
				return []
		for i in range(2):
			v.pop()
		c.sem = v.pop()
		if len(v) != 0:
			return [c] + parseRevClass(v)
		else:
			return [c]

	with open(fname) as f:
	    content = f.readlines()
	content = [line.strip() for line in content]
	ans = []
	for line in content:
		ret = parseRevClass(line.split()[::-1])
		ans += ret
	return ans

courses = []
def addNewCourse(name, credits, grade, sem):
	c = Course()
	c.name = name
	c.credits = int(credits)
	c.grade = float(grade)
	c.sem = sem
	courses.append(c)

def getCR():
	return getCRUntil('2S3016')

def getCRUntil(sem):
	num = 0.0
	den = 0
	pr = int(sem[0])
	year = int(sem[2:])
	for c in courses:
		cpr = int(c.sem[0])
		cyear = int(c.sem[2:])
		if cyear < year or (cyear == year and cpr <= pr):
			num += c.grade*c.credits
			den += c.credits
	cr = num/den/10
	return cr


def getSemCR(sem):
	num = 0.0
	den = 0
	pr = int(sem[0])
	year = int(sem[2:])
	for c in courses:
		cpr = int(c.sem[0])
		cyear = int(c.sem[2:])
		if cyear == year and cpr == pr:
			num += c.grade*c.credits
			den += c.credits
	cr = num/den/10
	return cr


def plot_charts():
	year = 2012
	pr = 1

	labels = []
	acc = []
	partial = []

	ignored = {'2S2015', '1S2016', '2S2018'}

	while year <= 2018:
		sem = str(pr) + 'S' + str(year)
		if sem not in ignored:
			cacc = getCRUntil(sem)
			cpartial = getSemCR(sem)
			print('%s: %.4f' % (sem, cacc))
			labels.append(sem)
			acc.append(cacc)
			partial.append(cpartial)
		pr += 1
		if pr == 3:
			pr = 1
			year += 1


	print(acc)
	print(partial)
	plt.plot(labels, acc)
	plt.plot(labels, partial)
	plt.legend(('Accumulated', 'Partial'))
	plt.xlabel('Semester')
	plt.ylabel('CR')
	plt.title('CR evolution')
	plt.show()

def main():
	global courses
	courses += parseFromFile('grades.txt')
	plot_charts()


if __name__ == "__main__":
    main()