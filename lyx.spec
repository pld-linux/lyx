Summary:	A WYSIWYM frontend to LaTeX
Summary(pl):	Nak³adka WYSIWYM na LaTeXa
Summary(pt_BR):	Editor de Textos para ambiente Desktop
Name:		lyx
Version:	1.3.0
Release:	2
Epoch:		1
License:	GPL
Group:		Applications/Publishing/TeX
Source0:	ftp://ftp.lyx.org/pub/lyx/stable/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-libconfigure.patch
Icon:		lyx.xpm
URL:		http://www.lyx.org/
BuildRequires:  Aiksaurus-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	tetex-fonts
BuildRequires:	qt-devel
BuildRequires:	aspell-devel
Prereq:		tetex
Requires:	gv
Requires:	python-modules
Requires:	tetex-fonts
Requires:	tetex-latex
Requires:	xdvi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pt_BR
Lyx é uma forma moderna de escrever documentos com um computador sem
que isso quebre os conceitos de uso de uma máquina de escrever
tradicional. Ele é feito para pessoas que necessitam de um resultado
profissional com um mínimo de esforço, sem também ser um especialista
em fontes. Comparado com um editor de textos padrão, LyX é um editor
de textos que irá aumentar a produtividade visto que as fontes serão
selecionadas pelo editor, não pelo digitador.

%prep
%setup -q
%patch0 -p1

%build
#rm -f acinclude.m4
#%%{__aclocal} -I config
#%%{__autoconf}
#cd lib/reLyX
#%%{__autoconf}
#cd ../..
#%%{__automake}
CXXFLAGS="%{rpmcflags} -fno-exceptions"
%configure \
	--enable-nls \
	--without-included-gettext \
	%{?!debug:--without-debug} \
	--with-frontend=qt \
	--with-pspell \
	--with-qt-includes=%{_includedir}/qt
	

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Office/Wordprocessors,%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Office/Wordprocessors
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

chmod a+rx $RPM_BUILD_ROOT%{_datadir}/lyx/configure

rm -f $RPM_BUILD_ROOT%{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}
ln -sf %{_datadir}/lyx/tex $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/lyx

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%{_bindir}/texhash
cd %{_datadir}/lyx/
./configure > /dev/null || :
if [ -f lyxrc.defaults ]; then
	cp -p lyxrc.defaults lyxrc
fi

%postun
%{_bindir}/texhash

%preun
rm -f %{_datadir}/lyx/{lyxrc.defaults,lyxrc*}
rm -f %{_datadir}/lyx/{doc/LaTeXConfig.lyx,packages.lst}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ANNOUNCE README NEWS
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/texmf/tex/latex/lyx
%attr(-, root,root) %{_datadir}/lyx
%{_mandir}/man*/*
%{_applnkdir}/Office/Wordprocessors/*
%{_pixmapsdir}/*
