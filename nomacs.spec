Summary:	Lightweight image viewer
Name:		nomacs
Version:	2.4.4
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/nomacs/%{name}-%{version}-source.tar.bz2
# Source0-md5:	88c1e2f9adc37bbd4c2fbbc4b7aabd37
Source1:	nomacs.appdata.xml
URL:		http://nomacs.org/
BuildRequires:	QtGui-devel >= 4.7
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	exiv2-devel >= 0.20
BuildRequires:	libraw-devel >= 0.12.0
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel >= 0.3.1
BuildRequires:	opencv-devel >= 2.1.0
BuildRequires:	quazip-devel >= 0.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nomacs is image viewer based on Qt4 library.

nomacs is small, fast and able to handle the most common image
formats. Additionally it is possible to synchronize multiple viewers
running on the same computer or via LAN is possible. It allows to
compare images and spot the differences e.g. schemes of architects to
show the progress).

%prep
%setup -q

dos2unix Readme/*

rm -r 3rdparty/libwebp
rm -r 3rdparty/quazip-0.7

%build
install -d build
cd build
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_FLAGS_RELEASE:STRING="-O2" \
	-DENABLE_RAW=1 \
	-DUSE_SYSTEM_WEBP=ON \
	-DUSE_SYSTEM_QUAZIP=ON \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# the "als" hack, see below
cp translations/nomacs_{az,als}.ts

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# hack - wrong lang code "als" (http://www.nomacs.org/redmine/issues/228)
# yes, the hack needs to be in make install, not in prep or build
rm translations/nomacs_als.ts
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/nomacs_als.qm

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
%doc Readme/[CLR]*
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/translations
%{_datadir}/appdata/%{name}.appdata.xml
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
