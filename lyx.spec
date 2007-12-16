Summary:	A WYSIWYM frontend to LaTeX
Summary(pl.UTF-8):	Nakładka WYSIWYM na LaTeXa
Summary(pt_BR.UTF-8):	Editor de Textos para ambiente Desktop
Name:		lyx
Version:	1.5.3
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Publishing/TeX
Source0:	ftp://ftp.lyx.org/pub/lyx/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	4fe013248713bb126877c317cad57238
Source1:	%{name}.desktop
Source2:	%{name}.png
URL:		http://www.lyx.org/
BuildRequires:	QtGui-devel
BuildRequires:	aiksaurus-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	boost-array-devel
BuildRequires:	boost-bind-devel
BuildRequires:	boost-crc-devel
BuildRequires:	boost-filesystem-devel
BuildRequires:	boost-regex-devel
BuildRequires:	boost-test-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	tetex
Requires:	gv
Requires:	python-modules
Requires:	tetex-latex
Requires:	xdvi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		texmfdir	%{_datadir}/texmf

%description
LyX is a modern approach of writing documents with a computer which
breaks with the tradition of the obsolete typewriter concept. It is
designed for people who want a professional output with a minimum of
time effort, without becoming specialists in typesetting. Compared to
common word processors LyX will increase the productivity a lot, since
most of the typesetting will be done by the computer, not the author.
With LyX the author can concentrate on the contents of his writing,
since the computer will take care of the look.

%description -l pl.UTF-8
LyX jest nowoczesnym narzędziem służącym do pisania dokumentów
łamiącym dotychczasową, przestarzałą tradycję maszyny do pisania. LyX
został zaprojektowany dla ludzi, którzy chcą tworzyć profesjonalne
dokumenty przy jak najmniejszym nakładzie czasowym bez konieczności
bycia specjalistą w składzie tekstów. LyX pozwala autorowi skupić się
na zawartości dokumentu podczas gdy komputer zajmie się całą resztą.

%description -l pt_BR.UTF-8
Lyx é uma forma moderna de escrever documentos com um computador sem
que isso quebre os conceitos de uso de uma máquina de escrever
tradicional. Ele é feito para pessoas que necessitam de um resultado
profissional com um mínimo de esforço, sem também ser um especialista
em fontes. Comparado com um editor de textos padrão, LyX é um editor
de textos que irá aumentar a produtividade visto que as fontes serão
selecionadas pelo editor, não pelo digitador.

%prep
%setup -q
%{__perl} -pi -e 's/-lqt-mt -lqt-mt3 -lqt3 -lqt2 -lqt/-lqt-mt/' config/qt.m4

%build
cat config/*.m4 > acinclude.m4
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-qt4-dir=%{_libdir}/qt4 \
	--enable-nls \
	--without-included-gettext \
	--without-included-boost \
	%{!?debug:--without-debug} \
	--with-frontend=qt4 \
	--with-qt-includes=%{_includedir}/qt \
	--with-pspell

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{texmfdir}/tex/latex

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

rm -f $RPM_BUILD_ROOT%{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}
ln -sf %{_datadir}/lyx/tex $RPM_BUILD_ROOT%{texmfdir}/tex/latex/lyx

sed -i -e 's,#! /usr/bin/env python,#!/usr/bin/python,' $RPM_BUILD_ROOT%{_datadir}/lyx/configure.py

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
/usr/bin/texhash
cd %{_datadir}/lyx
./configure.py > /dev/null || :
if [ -f lyxrc.defaults ]; then
	cp -p lyxrc.defaults lyxrc
fi

%preun
if [ "$1" = "0" ]; then
	rm -f %{_datadir}/lyx/{lyxrc.defaults,lyxrc*}
	rm -f %{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}
fi

%postun
umask 022
/usr/bin/texhash

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ANNOUNCE README NEWS
%attr(755,root,root) %{_bindir}/*
%dir %{texmfdir}/tex/latex/lyx
%dir %{_datadir}/lyx
%{_datadir}/lyx/CREDITS
%{_datadir}/lyx/bind
%{_datadir}/lyx/chkconfig.ltx
%{_datadir}/lyx/doc/clipart
%attr(755,root,root) %{_datadir}/lyx/configure*
%dir %{_datadir}/lyx/doc
%{_datadir}/lyx/doc/[A-Z]*
%lang(cs) %{_datadir}/lyx/doc/cs
%lang(da) %{_datadir}/lyx/doc/da
%lang(de) %{_datadir}/lyx/doc/de
%lang(es) %{_datadir}/lyx/doc/es
%lang(eu) %{_datadir}/lyx/doc/eu
%lang(fr) %{_datadir}/lyx/doc/fr
%lang(gl) %{_datadir}/lyx/doc/gl
%lang(he) %{_datadir}/lyx/doc/he
%lang(hu) %{_datadir}/lyx/doc/hu
%lang(it) %{_datadir}/lyx/doc/it
%lang(nb) %{_datadir}/lyx/doc/nb
%lang(nl) %{_datadir}/lyx/doc/nl
%lang(pl) %{_datadir}/lyx/doc/pl
%lang(pt) %{_datadir}/lyx/doc/pt
%lang(ro) %{_datadir}/lyx/doc/ro
%lang(ru) %{_datadir}/lyx/doc/ru
%lang(sk) %{_datadir}/lyx/doc/sk
%lang(sl) %{_datadir}/lyx/doc/sl
%lang(sv) %{_datadir}/lyx/doc/sv
%{_datadir}/lyx/encodings
%{_datadir}/lyx/examples
%{_datadir}/lyx/external_templates
%{_datadir}/lyx/fonts/
%{_datadir}/lyx/images
%{_datadir}/lyx/kbd
%{_datadir}/lyx/languages
%{_datadir}/lyx/layouts
%attr(755,root,root) %{_datadir}/lyx/lyx2lyx
%attr(755,root,root) %{_datadir}/lyx/scripts
%{_datadir}/lyx/symbols
%{_datadir}/lyx/syntax.default
%{_datadir}/lyx/templates
%{_datadir}/lyx/tex
%{_datadir}/lyx/ui
%{_datadir}/lyx/unicodesymbols
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
