SLUG = unipain

SLIDE_HTML = $(SLUG).html

SUPPORT = lineselect.js Symbola.ttf

.PHONY: $(SLIDE_HTML)

slides: $(SLIDE_HTML)

PNG_DIR = png

$(SLIDE_HTML): *.py 
	\\vpy\\unipain\\27\\Scripts\\python.exe -m cogapp -U -r $@
	\\vpy\\unipain\\32\\Scripts\\python.exe -m cogapp -U -r $@

%.out : %.py
	echo "$$ python $*.py" > $@
	-python $*.py >> $@ 2>&1

clean:
	rm -f *.pyc $(PX)
	rm -rf __pycache__
	rm -rf $(PNG_DIR)

pngs:
	phantomjs phantom-slippy-to-png.js $(SLIDE_HTML) $(PNG_DIR)/

PX = $(SLUG).px

px $(PX): $(SLIDE_HTML)
	python slippy_to_px.py $(SLIDE_HTML) $(PX) $(SLUG)

WEBHOME = ~/web/stellated/pages/text
WEBPREZHOME = $(WEBHOME)/$(SLUG)
WEBPIXHOME = $(WEBHOME)/$(SLUG)_pix

publish: $(PX) pngs
	mkdir -p $(WEBPREZHOME) $(WEBPIXHOME)
	cp -f $(PX) $(WEBHOME)
	cp -f $(PNG_DIR)/* $(WEBPIXHOME)
	cp -f $(SLIDE_HTML) $(SUPPORT) $(WEBPREZHOME)
	cp -fR slippy $(WEBPREZHOME)
	cp -fR highlight $(WEBPREZHOME)
