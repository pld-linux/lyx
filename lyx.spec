Summary:	A WYSIWYM frontend to LaTeX
Summary(pl):	Nak³adka WYSIWYM na LaTeXa
Name:		lyx
Version:	1.1.4
Release:	1
Source0:	ftp://ftp.lyx.org/pub/lyx/stable/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Patch0:		ftp://ftp.lyx.org/pub/lyx/devel/stable/patch-1.1.4fix1.gz
Patch1:		ftp://ftp.lyx.org/pub/lyx/devel/stable/patch-1.1.4fix2.gz
License:	GPL
Group:		Applications/Publishing/TeX
Group(pl):	Aplikacje/Publikowanie/TeX
Requires: 	xforms >= 0.88,
Requires:	gv
Requires:	xdvi
Requires:	tetex-latex
URL:		http://www.lyx.org/
Buildroot:	/tmp/%{name}-%{version}-root

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
LyX is a modern approach of writing documents with a computer which breaks
with the tradition of the obsolete typewriter concept. It is designed for
people who want a professional output with a minimum of time effort,
without becoming specialists in typesetting.  Compared to common word
processors LyX will increase the productivity a lot, since most of the
typesetting will be done by the computer, not the author.  With LyX the
author can concentrate on the contents of his writing, since the computer
will take care of the look.

%description -l pl
LyX jest nowoczesnym narzêdziem s³u¿±cym do pisania dokumentów ³ami±cym
dotychczasow±, przestarza³± tradycjê maszyny do pisania. LyX zosta³
zaprojektowany dla ludzi, którzy chc± tworzyæ profesjonalne dokumenty przy
jak najmniejszym nak³adzie czasowym bez konieczno¶ci bycia specjalist± w
sk³adzie tekstów.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-s"; export LDFLAGS
aclocal
%configure \
	--without-included-gettext \
	--enable-nls \
	--without-debug

make all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/applnk/Applications

make install DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT \

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applnk/Applications

gzip -9nf ANNOUNCE CHANGES README UPGRADING WHATSNEW \
	$RPM_BUILD_ROOT%{_mandir}/man1/*

%find_lang %{name}

%post
cd %{_datadir}/lyx/
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
%config(missingok) %{_datadir}/applnk/Applications/*
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
