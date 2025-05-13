.PHONY: dirs all clean

ifdef OS
   RM = rmdir /s /q
else
   ifeq ($(shell uname), Linux)
      RM = rm -rf
   endif
endif

dirs:
	@mkdir "./data/"

	@mkdir "./results/"
	
	@echo Data directories created.

all: dirs
	echo All done.

clean:
	@$(RM) "./data/"
	@$(RM) "./results/"
	@echo Clean done.
