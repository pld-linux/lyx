Summary:	A WYSIWYM frontend to LaTeX
Summary(pl):	Nak³adka WYSIWYM na LaTeXa
Name:		lyx
Version:	1.1.6
Release:	1
License:	GPL
Group:		Applications/Publishing/TeX
Group(de):	Applikationen/Publizieren/TeX
Group(pl):	Aplikacje/Publikowanie/TeX
Source0:	ftp://ftp.lyx.org/pub/lyx/stable/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Icon:		lyx.xpm
Requires:	gv
Requires:	xdvi
Requires:	tetex
Requires:	tetex-latex
BuildRequires:	xforms-devel >= 0.88
BuildRequires:	XFree86-devel
BuildRequires:	libstdc++-devel
URL:		http://www.lyx.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_old_bindir	/usr/bin
%define		_old_datadir	/usr/share
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
LyX is a modern approach of writing documents with a computer which
breaks with the tradition of the obsolete typewriter concept. It is
designed for people who want a professional output with a minimum of
time effort, without becoming specialists in typesetting. Compared to
common word processors LyX will increase the productivity a lot, since
most of the typesetting will be done by the computer, not the author.
With LyX the author can concentrate on the contents of his writing,
since the computer will take care of the look.

%description -l pl
LyX jest nowoczesnym narzêdziem s³u¿±cym do pisania dokumentów
³ami±cym dotychczasow±, przestarza³± tradycjê maszyny do pisania. LyX
zosta³ zaprojektowany dla ludzi, którzy chc± tworzyæ profesjonalne
dokumenty przy jak najmniejszym nak³adzie czasowym bez konieczno¶ci
bycia specjalist± w sk³adzie tekstów. LyX pozwala autorowi skupiæ siê
na zawarto¶ci dokumentu podczas gdy komputer zajmie siê ca³± reszt±.

%prep
%setup -q

%build
CXXFLAGS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS} -fno-rtti -fno-exceptions"
%configure \
	--enable-nls \
	--without-included-gettext \
	--without-debug \

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Office/Editors,%{_datadir}/pixmaps} \
	$RPM_BUILD_ROOT%{_old_datadir}/texmf/tex/latex/

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	localedir=$RPM_BUILD_ROOT%{_datadir}/locale \
	gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Office/Editors
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/pixmaps

rm -f $RPM_BUILD_ROOT%{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}
ln -s %{_datadir}/lyx/tex $RPM_BUILD_ROOT%{_old_datadir}/texmf/tex/latex/lyx

gzip -9nf ANNOUNCE README NEWS

%find_lang %{name}

%post
umask 022
%{_old_bindir}/texhash
cd %{_datadir}/lyx/
./configure > /dev/null
if [ -f lyxrc.defaults ]; then
	cp -p lyxrc.defaults lyxrc
fi

%postun
%{_old_bindir}/texhash

%preun
rm -f %{_datadir}/lyx/{lyxrc.defaults,lyxrc*}
rm -f %{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {ANNOUNCE,README,NEWS}.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_old_datadir}/texmf/tex/latex/lyx
%attr(-, root,root) %{_datadir}/lyx
%{_mandir}/man*/*
%{_applnkdir}/Office/Editors/*
%{_datadir}/pixmaps/*
