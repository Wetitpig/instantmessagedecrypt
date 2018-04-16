SUBDIRS = wechat

PROCESSES = all clean install uninstall

$(PROCESSES):
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir $@; \
	done
