Summary:     A WYSIWYG frontend to LaTeX
Name:        lyx
Version:     1.0.3
Release:     1
Source0:     ftp://ftp.via.ecp.fr/pub/lyx/devel/stable/%{name}-%{version}.tar.gz
Source1:     %{name}.wmconfig
Serial:      01000002
Copyright:   GPL
Group:       X11/Applications/Publishing
Requires:    xforms >= 0.88, gv, tetex-xdvi, tetex, tetex-latex
URL:         http://www.lyx.org/
Buildroot:   /tmp/%{name}-%{version}-root

%description
LyX is a modern approach of writing documents with a computer which breaks
with the tradition of the obsolete typewriter concept. It is designed for
people who want a professional output with a minimum of time effort, without
becoming specialists in typesetting.  Compared to common word processors LyX
will increase the productivity a lot, since most of the typesetting will be
done by the computer, not the author.  With LyX the author can concentrate
on the contents of his writing, since the computer will take care of the
look.

%prep
%setup -q

%build
CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=/usr/X11R6 \
	--with-gnu-gettext \
	--enable-nls \
	--without-debug

make all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/X11/wmconfig

make install \
	prefix=$RPM_BUILD_ROOT/usr/X11R6

strip $RPM_BUILD_ROOT/usr/X11R6/bin/lyx

install %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/wmconfig/lyx
gzip -9nf $RPM_BUILD_ROOT/usr/X11R6/man/man1/*

rm -f $RPM_BUILD_ROOT/usr/X11R6/share/lyx/{doc/LaTeXConfig.lyx,packages.lst}

%find_lang %{name}

%post
cd /usr/X11R6/share/lyx/
./configure > /dev/null
if [ -f lyxrc.defaults ]; then
	cp lyxrc.defaults lyxrc
fi

%preun
rm -f /usr/X11R6/share/lyx/{lyxrc.defaults,lyxrc*}
rm -f /usr/X11R6/share/lyx/{doc/LaTeXConfig.lyx,packages.lst}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ANNOUNCE APPLIED_PATCHES BUGS CHANGES README TODO
%config(missingok) /etc/X11/wmconfig/*
%attr(755,root,root) /usr/X11R6/bin/*
/usr/X11R6/man/man1/*
%dir /usr/X11R6/share/lyx
%attr(755,root,root) /usr/X11R6/share/lyx/configure
/usr/X11R6/share/lyx/chkconfig.ltx
/usr/X11R6/share/lyx/CREDITS
/usr/X11R6/share/lyx/bind
/usr/X11R6/share/lyx/clipart
%dir /usr/X11R6/share/lyx/doc
/usr/X11R6/share/lyx/doc/*.lyx
/usr/X11R6/share/lyx/doc/LaTeXConfig.lyx.in
/usr/X11R6/share/lyx/doc/*.eps
/usr/X11R6/share/lyx/examples
/usr/X11R6/share/lyx/kbd
/usr/X11R6/share/lyx/images
/usr/X11R6/share/lyx/layouts
/usr/X11R6/share/lyx/reLyX
/usr/X11R6/share/lyx/templates
/usr/X11R6/share/lyx/tex
