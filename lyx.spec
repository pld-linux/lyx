Summary:	A WYSIWYG frontend to LaTeX
Name:		lyx
Version:	1.0.3
Release:	1
Source0:	ftp://ftp.via.ecp.fr/pub/lyx/devel/stable/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Patch:		lyx-DESTDIR.patch
Serial:		01000003
Copyright:	GPL
Group:		X11/Applications/Publishing
Requires:	xforms >= 0.88, gv, tetex-xdvi, tetex, tetex-latex
URL:		http://www.lyx.org/
Buildroot:	/tmp/%{name}-%{version}-root

%define		_prefix	/usr/X11R6
%define		_mandir /usr/X11R6/man

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
%patch -p1

%build
%configure \
	--with-gnu-gettext \
	--enable-nls \
	--without-debug

make all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/X11/applnk/Applications

make install DESTDIR=$RPM_BUILD_ROOT \
	localedir=$RPM_BUILD_ROOT%{_datadir}/locale \
	gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

install %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/applnk/Applications

rm -f $RPM_BUILD_ROOT%{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}

strip $RPM_BUILD_ROOT%{_bindir}/lyx

gzip -9nf ANNOUNCE CHANGES README UPGRADING WHATSNEW \
	$RPM_BUILD_ROOT%{_mandir}/man1/*

%find_lang %{name}

%post
cd /usr/X11R6/share/lyx/
./configure > /dev/null
if [ -f lyxrc.defaults ]; then
	cp lyxrc.defaults lyxrc
fi

%preun
rm -f %{_datadir}/lyx/{lyxrc.defaults,lyxrc*}
rm -f %{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {ANNOUNCE,CHANGES,README,UPGRADING,WHATSNEW}.gz
%config(missingok) /etc/X11/applnk/Applications/*
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/lyx
%dir %{_datadir}/lyx/doc
%attr(755,root,root) %{_datadir}/lyx/configure
%{_datadir}/lyx/chkconfig.ltx
%{_datadir}/lyx/CREDITS
%{_datadir}/lyx/bind
%{_datadir}/lyx/clipart
%{_datadir}/lyx/doc/*.lyx
%{_datadir}/lyx/doc/LaTeXConfig.lyx.in
%{_datadir}/lyx/doc/*.eps
%{_datadir}/lyx/examples
%{_datadir}/lyx/kbd
%{_datadir}/lyx/images
%{_datadir}/lyx/layouts
%{_datadir}/lyx/reLyX
%{_datadir}/lyx/templates
%{_datadir}/lyx/tex
%{_mandir}/man1/*
