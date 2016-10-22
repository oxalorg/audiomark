encode:
	python3 audiomark.py --encode --message "$(msg)"

decode:
	gcc decode.c -lsndfile && ./a.out


