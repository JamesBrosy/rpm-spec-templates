#
# spec file for package wps-office-missing-fonts
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}
%global         pkgname wps-office-missing-fonts

Name:           %{pkgname}
Version:        VERSION
Release:        1%{?dist}
Summary:        WPS Office missing fonts

License:        MIT
URL:            https://github.com/JamesBrosy/wps-office-fix
Source0:        %{url}/archive/v%{version}/wps-office-fix-%{version}.tar.gz

BuildArch:      noarch

%description
Fix missing fonts for WPS Office

%prep
tar xf %{SOURCE0}

%build

%install
cd wps-office-fix-%{version}
for font in fonts/*.ttf; do
  install -Dm644 "$font" -t %{buildroot}%{_datadir}/fonts/wps-office
done

%files
%license wps-office-fix-%{version}/LICENSE
%dir %{_datadir}/fonts/wps-office
%{_datadir}/fonts/wps-office/*.ttf

%changelog
* DATE Jo Carllyle
- See GitHub for full changelog
