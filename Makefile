.PHONY: dirs downloads all clean

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

downloads:
	gdown 1DFsAF4MED8ZUKhio79yeiC0zhvB4j-Oq -O ./data/knapsack-instance.txt

all: dirs downloads
	echo All done.

clean:
	@$(RM) "./data/"
	@$(RM) "./results/"
	@echo Clean done.
