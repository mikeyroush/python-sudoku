def isTouched(obj,point):
	(x,y) = point
	(X,Y) = obj.position
	bound = obj.size.w/2
	return X - bound < x and X + bound > x and Y - bound < y and Y + bound > y
