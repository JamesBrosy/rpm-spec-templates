#
# spec file for package wps-office-fix
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}
%global         pkgname wps-office-fix

Name:           %{pkgname}
Version:        VERSION
Release:        1%{?dist}
Summary:        WPS Office Fix

License:        MIT and others
URL:            https://github.com/JamesBrosy/%{pkgname}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Requires:       wps-office-fix-missing-fonts, wps-office-fix-libfreetype

%description
Fix some problems of WPS Office after installation

%package        missing-fonts
Summary:        WPS Office missing fonts

%description    missing-fonts
WPS Office missing fonts

%package        libfreetype
Summary:        WPS Office freetype library

%description    libfreetype
WPS Office freetype library

%prep
%autosetup

%build

%install
for font in fonts/*.ttf; do
  install -Dm644 "$font" -t %{buildroot}%{_datadir}/fonts/wps-office
done

install -Dm755 libfreetype/%{_arch}/libfreetype* -t %{buildroot}/opt/kingsoft/wps-office/office6

cd %{buildroot}/opt/kingsoft/wps-office/office6 && ln -s libfreetype.so.6.18.3 libfreetype.so.6 && cd -

%files
%license LICENSE

%files missing-fonts
%license LICENSE
%dir %{_datadir}/fonts/wps-office
%{_datadir}/fonts/wps-office/*.ttf

%files libfreetype
%license LICENSE
%dir /opt/kingsoft
/opt/kingsoft/*

%changelog
* DATE Jo Carllyle <JamesBrosy@users.noreply.github.com>
- See GitHub for full changelog
