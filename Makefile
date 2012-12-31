SLIDE_HTML = unipain.html

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
	\\app\\phantomjs-1.3.0-win32-dynamic\\phantomjs.exe phantom-slippy-to-png.js $(SLIDE_HTML) $(PNG_DIR)/

PX = unipain.px

px $(PX): $(SLIDE_HTML)
	python slippy_to_px.py $(SLIDE_HTML) $(PX)

WEBHOME = c:/ned/web/stellated/pages/text
WEBPREZHOME = $(WEBHOME)/unipain

publish: $(PX) pngs
	cp -f $(PX) $(WEBHOME)
	cp -f $(PNG_DIR)/* $(WEBHOME)
	cp -f $(SLIDE_HTML) $(SUPPORT) $(WEBPREZHOME)
	svn export --force slippy $(WEBPREZHOME)/slippy
	svn export --force highlight $(WEBPREZHOME)/highlight
