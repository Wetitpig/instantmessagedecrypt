SUBDIRS = wechat

PROCESSES = all clean install

$(PROCESSES):
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir $@; \
	done
