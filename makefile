all:
	make -f wattsfarmer.mk
	make -f repeat-a.mk
	make -f masterballs.mk
	make -f wildareabreeding.mk
	make -f releasebox.mk

watts:
	make -f wattsfarmer.mk

repeat-a:
	make -f repeat-a.mk

balls:
	make -f masterballs.mk

wildarea:
	make -f wildareabreeding.mk

release:
	make -f releasebox.mk