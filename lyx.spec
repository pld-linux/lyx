Summary:	A WYSIWYM frontend to LaTeX
Summary(pl):	Nak�adka WYSIWYM na LaTeXa
Summary(pt_BR):	Editor de Textos para ambiente Desktop
Name:		lyx
Version:	1.4.0
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Publishing/TeX
Source0:	ftp://ftp.lyx.org/pub/lyx/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	5ab37471339ff7dbc8f0c43282746cb0
Source1:	%{name}.desktop
Source2:	%{name}.png
# it's patch from BRANCH_1_3_X
Patch0:		%{name}-libconfigure.patch
URL:		http://www.lyx.org/
BuildRequires:	XFree86-devel
BuildRequires:	aiksaurus-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	libstdc++-devel
BuildRequires:  rpm-pythonprov
BuildRequires:	qt-devel
# for xfonts generation
BuildRequires:	kpathsea
BuildRequires:	tetex-fonts-type1-bluesky
BuildRequires:	tetex-fonts-type1-hoekwater
PreReq:		tetex
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

%description -l pl
LyX jest nowoczesnym narz�dziem s�u��cym do pisania dokument�w
�ami�cym dotychczasow�, przestarza�� tradycj� maszyny do pisania. LyX
zosta� zaprojektowany dla ludzi, kt�rzy chc� tworzy� profesjonalne
dokumenty przy jak najmniejszym nak�adzie czasowym bez konieczno�ci
bycia specjalist� w sk�adzie tekst�w. LyX pozwala autorowi skupi� si�
na zawarto�ci dokumentu podczas gdy komputer zajmie si� ca�� reszt�.

%description -l pt_BR
Lyx � uma forma moderna de escrever documentos com um computador sem
que isso quebre os conceitos de uso de uma m�quina de escrever
tradicional. Ele � feito para pessoas que necessitam de um resultado
profissional com um m�nimo de esfor�o, sem tamb�m ser um especialista
em fontes. Comparado com um editor de textos padr�o, LyX � um editor
de textos que ir� aumentar a produtividade visto que as fontes ser�o
selecionadas pelo editor, n�o pelo digitador.

%prep
%setup -q
%patch0 -p1

%{__perl} -pi -e 's/-lqt-mt -lqt-mt3 -lqt3 -lqt2 -lqt/-lqt-mt/' config/qt.m4

%build
./autogen.sh
cp -f /usr/share/automake/config.* config
CXXFLAGS="%{rpmcflags} -fno-exceptions"
%configure \
	--enable-nls \
	--without-included-gettext \
	%{?!debug:--without-debug} \
	--with-frontend=qt \
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

chmod a+rx $RPM_BUILD_ROOT%{_datadir}/lyx/configure

rm -f $RPM_BUILD_ROOT%{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}
ln -sf %{_datadir}/lyx/tex $RPM_BUILD_ROOT%{texmfdir}/tex/latex/lyx

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
/usr/bin/texhash
cd %{_datadir}/lyx
./configure > /dev/null || :
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
%{_datadir}/lyx/clipart
%attr(755,root,root) %{_datadir}/lyx/configure*
%dir %{_datadir}/lyx/doc
%{_datadir}/lyx/doc/[A-Z]*
%{_datadir}/lyx/doc/*.eps
%lang(cs) %{_datadir}/lyx/doc/cs_*
%lang(da) %{_datadir}/lyx/doc/da_*
%lang(de) %{_datadir}/lyx/doc/de_*
%lang(es) %{_datadir}/lyx/doc/es_*
%lang(eu) %{_datadir}/lyx/doc/eu_*
%lang(fr) %{_datadir}/lyx/doc/fr_*
%lang(he) %{_datadir}/lyx/doc/he_*
%lang(hu) %{_datadir}/lyx/doc/hu_*
%lang(it) %{_datadir}/lyx/doc/it_*
%lang(nb) %{_datadir}/lyx/doc/nb_*
%lang(nl) %{_datadir}/lyx/doc/nl_*
%lang(pl) %{_datadir}/lyx/doc/pl_*
%lang(pt) %{_datadir}/lyx/doc/pt_*
%lang(ro) %{_datadir}/lyx/doc/ro_*
%lang(ru) %{_datadir}/lyx/doc/ru_*
%lang(sk) %{_datadir}/lyx/doc/sk_*
%lang(sl) %{_datadir}/lyx/doc/sl_*
%lang(sv) %{_datadir}/lyx/doc/sv_*
%{_datadir}/lyx/encodings
%{_datadir}/lyx/examples
%{_datadir}/lyx/external_templates
%{_datadir}/lyx/images
%{_datadir}/lyx/kbd
%{_datadir}/lyx/languages
%{_datadir}/lyx/layouts
%attr(755,root,root) %{_datadir}/lyx/lyx2lyx
%{_datadir}/lyx/lyxrc.*
%attr(755,root,root) %{_datadir}/lyx/scripts
%{_datadir}/lyx/symbols
%{_datadir}/lyx/syntax.default
%{_datadir}/lyx/templates
%{_datadir}/lyx/tex
%{_datadir}/lyx/textclass.lst
%{_datadir}/lyx/ui
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
