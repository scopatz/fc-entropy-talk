notebook = fc-entropy-talk
nbcdir = ~/nbconvert

all:
	cp -r $(nbcdir)/reveal . $<
	rm -rf reveal/.git* $<
	mkdir -p js $<
	cp $(nbcdir)/js/mathjax-onload.js js
	cp classy.css reveal/css/theme/ $<
	python $(nbcdir)/nbconvert.py -f reveal $(notebook).ipynb $<
	sed -i 's:reveal/css/theme/simple.css:reveal/css/theme/classy.css:' fc-entropy-talk_slides.html $<
	sed -i 's:class="fragment" class="text_cell_render:class="fragment text_cell_render:' fc-entropy-talk_slides.html $<
	sed -i 's/.rendered_html ul{list-style:disc;margin:1em 2em;}/.rendered_html ul{list-style:disc;margin:0em 2em;}/' fc-entropy-talk_slides.html $<

clean:
	rm -f *.pdf *.html *.zip

%.ps :%.eps
	convert $< $@

%.png :%.eps
	convert $< $@

zip:
	zip paper.zip *.html *.bib

.PHONY: all clean
