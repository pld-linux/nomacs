# TODO: system qpsd (http://sourceforge.net/projects/libqpsd/)
#
# Conditional build:
%bcond_with	qt5	# use Qt 5 instead of 4
#
%define	qt4_ver	4.7.0
Summary:	Lightweight image viewer
Summary(pl.UTF-8):	Lekka przeglądarka obrazków
Name:		nomacs
Version:	2.4.6
Release:	3
License:	GPL v3+
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/nomacs/%{name}-%{version}-source.tar.bz2
# Source0-md5:	a154966dc5c1fed71279bc70d8078935
Source1:	%{name}.appdata.xml
URL:		http://nomacs.org/
BuildRequires:	cmake >= 2.6
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	exiv2-devel >= 0.20
BuildRequires:	libraw-devel >= 0.12.0
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel >= 0.3.1
BuildRequires:	opencv-devel >= 2.1.0
BuildRequires:	pkgconfig
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-linguist >= 5
BuildRequires:	qt5-qmake >= 5
BuildRequires:	quazip-qt5-devel >= 0.7
%else
BuildRequires:	QtCore-devel >= %{qt4_ver}
BuildRequires:	QtGui-devel >= %{qt4_ver}
BuildRequires:	QtNetwork-devel >= %{qt4_ver}
BuildRequires:	qt4-build >= %{qt4_ver}
BuildRequires:	qt4-linguist >= %{qt4_ver}
BuildRequires:	qt4-qmake >= %{qt4_ver}
BuildRequires:	quazip-devel >= 0.7
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nomacs is image viewer based on Qt 4 library.

nomacs is small, fast and able to handle the most common image
formats. Additionally it is possible to synchronize multiple viewers
running on the same computer or via LAN is possible. It allows to
compare images and spot the differences e.g. schemes of architects to
show the progress).

%description -l pl.UTF-8
nomacs to przeglądarka obrazków oparta na bibliotece Qt 4.

nomacs jest mała, szybka i potrafi obsłużyć większość popularnych
formatów obrazów. Ponadto możliwa jest synchronizacja wielu
przeglądarek działających na tym samym komputerze lub poprzez sieć
lokalną. Przeglądarka pozwala porównywać obrazki i wskazywać różnice,
np. projekty architektów w celu pokazania postępów.

%prep
%setup -q

dos2unix Readme/*

%{__rm} -r 3rdparty/libwebp
%{__rm} -r 3rdparty/quazip-0.7

%build
install -d build
cd build
%cmake \
	%{?with_qt5:-DENABLE_QT5} \
	-DENABLE_RAW=1 \
	-DUSE_SYSTEM_WEBP=ON \
	-DUSE_SYSTEM_QUAZIP=ON \
	..
# -DUSE_SYSTEM_LIBQPSD=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# translation to German "Vorarlbergerisch" dialect - should be de_AT@Vorarlberg?
# ("als" is wrong code - it's Tosk Albanian in iso-639-3)
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/nomacs_als.qm

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

install -d $RPM_BUILD_ROOT%{_datadir}/appdata
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml

%find_lang %{name} --with-qm --without-mo

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc Readme/{COPYRIGHT,LICENSE.OPENCV,README}
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/translations
%{_datadir}/appdata/%{name}.appdata.xml
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
