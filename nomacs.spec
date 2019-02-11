# TODO: add plugins (https://github.com/nomacs/nomacs-plugins/)
Summary:	Lightweight image viewer
Summary(pl.UTF-8):	Lekka przeglądarka obrazków
Name:		nomacs
Version:	3.12
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/nomacs/nomacs/archive/%{version}/%{name}-%{version}-source.tar.gz
# Source0-md5:	7b2160cbcf907ee080d696c61b3dc4e8
Patch0:		%{name}-libqpsd.patch
URL:		http://nomacs.org/
BuildRequires:	Qt5Concurrent-devel >= 5.2.1
BuildRequires:	Qt5Core-devel >= 5.2.1
BuildRequires:	Qt5Gui-devel >= 5.2.1
BuildRequires:	Qt5Network-devel >= 5.2.1
BuildRequires:	Qt5Svg-devel >= 5.2.1
BuildRequires:	cmake >= 2.8
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	exiv2-devel >= 0.25
BuildRequires:	libqpsd-qt5-devel
BuildRequires:	libraw-devel >= 0.17
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libtiff-devel
BuildRequires:	libtiff-cxx-devel
BuildRequires:	libwebp-devel >= 0.3.1
BuildRequires:	opencv-devel >= 2.4.6
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5.2.1
BuildRequires:	qt5-linguist >= 5.2.1
BuildRequires:	qt5-qmake >= 5.2.1
BuildRequires:	quazip-qt5-devel >= 0.7
Requires:	Qt5Concurrent >= 5.2.1
Requires:	Qt5Core >= 5.2.1
Requires:	Qt5Gui >= 5.2.1
Requires:	Qt5Network >= 5.2.1
Requires:	Qt5Svg >= 5.2.1
Requires:	exiv2-libs >= 0.25
Requires:	libraw >= 0.17
Requires:	opencv >= 2.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libnomacsCore.so.*
%description
nomacs is image viewer based on Qt library.

nomacs is small, fast and able to handle the most common image
formats. Additionally it is possible to synchronize multiple viewers
running on the same computer or via LAN is possible. It allows to
compare images and spot the differences e.g. schemes of architects to
show the progress).

%description -l pl.UTF-8
nomacs to przeglądarka obrazków oparta na bibliotece Qt.

nomacs jest mała, szybka i potrafi obsłużyć większość popularnych
formatów obrazów. Ponadto możliwa jest synchronizacja wielu
przeglądarek działających na tym samym komputerze lub poprzez sieć
lokalną. Przeglądarka pozwala porównywać obrazki i wskazywać różnice,
np. projekty architektów w celu pokazania postępów.

%prep
%setup -q
cd ImageLounge
%patch0 -p1

%{__rm} -r 3rdparty/libqpsd

%build
install -d build
cd build
%cmake ../ImageLounge \
	-DENABLE_PLUGINS=ON \
	-DENABLE_RAW=1 \
	-DUSE_SYSTEM_LIBQPSD=ON \
	-DUSE_SYSTEM_QUAZIP=ON \
	-DUSE_SYSTEM_WEBP=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# API not exported, so keep only library files + soname symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnomacs*.so

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database

%postun
/sbin/ldconfig
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc ImageLounge/Readme/{COPYRIGHT,LICENSE.OPENCV,README}
%attr(755,root,root) %{_bindir}/nomacs
%attr(755,root,root) %{_libdir}/libnomacsCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnomacsCore.so.3
%{_mandir}/man1/nomacs.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Image*
%{_datadir}/metainfo/nomacs.appdata.xml
%{_desktopdir}/nomacs.desktop
%{_pixmapsdir}/nomacs.svg
