#
# spec file for package neohtop
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}
%global         __brp_mangle_shebangs %{nil}


Name:           neohtop
Version:        VERSION
Release:        1%{?dist}
Summary:        A cross-platform system monitor

License:        MIT
URL:            https://github.com/abdenasser/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        NeoHtop.desktop

BuildRequires:  cargo
BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
%if 0%{?suse_version}
BuildRequires:  npm, libopenssl-devel, webkit2gtk3-devel
%else
BuildRequires:  nodejs, openssl-devel, webkit2gtk4.1-devel >= 2.40
%endif

%if 0%{?suse_version}
Requires:       libwebkit2gtk-4_1-0
%else
Requires:       webkit2gtk4.1 >= 2.40
%endif

%description
A cross-platform system monitor


%prep
%autosetup


%build
npm install
npm run tauri build


%install
install -Dsm755 src-tauri/target/release/NeoHtop -t %{buildroot}%{_bindir}
install -Dpm644 %{SOURCE1}                          %{buildroot}%{_datadir}/applications/NeoHtop.desktop
install -Dpm644 src-tauri/icons/128x128@2x.png      %{buildroot}%{_iconsdir}/hicolor/256x256@2/apps/NeoHtop.png
install -Dpm644 src-tauri/icons/32x32.png           %{buildroot}%{_iconsdir}/hicolor/32x32/apps/NeoHtop.png
install -Dpm644 src-tauri/icons/128x128.png         %{buildroot}%{_iconsdir}/hicolor/128x128/apps/NeoHtop.png

%files
%doc README.md
%license LICENSE
%{_bindir}/NeoHtop
%{_datadir}/icons/*
%{_datadir}/applications/*


%changelog
* DATE Abdenasser Elidrissi <nasser.elidrissi065@gmail.com>
- See GitHub for full changelog 
