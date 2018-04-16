PREFIX = /data/data/com.termux/files
INCLUDE = $(PREFIX)/usr/include
LD = $(PREFIX)/usr/lib

CC = gcc
CFLAGS = -O3 -I. -I$(INCLUDE)
LDFLAGS = -L$(LD) -lwcdb
HEADER = mm_backup.h

targets = dbbackup dbrepair

%: %.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

install:
	cp $(targets) $(PREFIX)/home
	cp decrypt.py $(PREFIX)/home/storage/shared/tencent

uninstall:
	for f in $(target); do \
		rm $(PREFIX)/home/$$f; \
	done
	rm $(PREFIX)/home/storage/shared/tencent/decrypt.py

clean:
	rm -f $(targets)

all: $(targets)
