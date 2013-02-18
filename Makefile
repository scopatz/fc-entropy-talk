notebook = fc-entropy-talk
nbcdir = ~/nbconvert

all:
	cp -r $(nbcdir)/reveal . $<
	rm -rf reveal/.git* $<
	cp classy.css reveal/css/theme/ $<
	python $(nbcdir)/nbconvert.py -f reveal $(notebook).ipynb $<
	sed -i 's:reveal/css/theme/simple.css:reveal/css/theme/classy.css:' fc-entropy-talk_slides.html $<

clean:
	rm -f *.pdf *.html *.zip

%.ps :%.eps
	convert $< $@

%.png :%.eps
	convert $< $@

zip:
	zip paper.zip *.html *.bib

.PHONY: all clean
