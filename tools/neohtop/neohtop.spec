#
# spec file for package neohtop
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%ifarch         x86_64
%define         arch1 x64
%define         arch2 amd64
%endif
%ifarch         aarch64
%define         arch1 arm64
%define         arch2 arm64
%endif

Name:           NeoHtop
Version:        VERSION
Release:        1%{?dist}
Summary:        A cross-platform system monitor

License:        MIT
URL:            https://abdenasser.github.io/neohtop
Source0:        https://github.com/Abdenasser/neohtop/archive/v%{version}/neohtop-%{version}.tar.gz

%if 0%{?suse_version}
BuildRequires:  cairo-devel, atkmm-devel, libopenssl-devel, pango-devel, gtk3-devel, libsoup-devel, webkit2gtk3-devel, librsvg-devel
%else
BuildRequires:  openssl-devel, gtk3-devel, webkit2gtk4.1-devel >= 2.40, libsoup3-devel, javascriptcoregtk4.1-devel, librsvg2-devel
%endif

BuildRequires:  gcc, tar, xz, jq
BuildRequires:  glib2-devel
%if 0%{?suse_version}
Requires:       libwebkit2gtk-4_1-0
%else
Requires:       webkit2gtk4.1 >= 2.40, javascriptcoregtk4.1
%endif

%description
A cross-platform system monitor


%prep
%autosetup


%build
# setup node
NODE_LTS=$(curl -s https://nodejs.org/dist/index.json | jq -r '[.[] | select(.lts != false)][0].version')
curl -L -O https://nodejs.org/dist/${NODE_LTS}/node-${NODE_LTS}-linux-%{arch1}.tar.xz
xz -d node-${NODE_LTS}-linux-%{arch1}.tar.xz
tar xf node-${NODE_LTS}-linux-%{arch1}.tar
export PATH="$(pwd)/node-${NODE_LTS}-linux-%{arch1}/bin:$PATH"
# setup rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# install dependencies
npm i
# build
npm run tauri build -- --target %{_arch}-unknown-linux-gnu --bundles deb


%install
install -Dsm755 src-tauri/target/%{_arch}-unknown-linux-gnu/release/%{name} -t %{buildroot}%{_bindir}
install -Dm644  src-tauri/target/%{_arch}-unknown-linux-gnu/release/bundle/deb/%{name}_%{version}_%{arch2}/data/usr/share/applications/%{name}.desktop              -t %{buildroot}%{_datadir}/applications
install -Dm644  src-tauri/target/%{_arch}-unknown-linux-gnu/release/bundle/deb/%{name}_%{version}_%{arch2}/data/usr/share/icons/hicolor/128x128/apps/%{name}.png    -t %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -Dm644  src-tauri/target/%{_arch}-unknown-linux-gnu/release/bundle/deb/%{name}_%{version}_%{arch2}/data/usr/share/icons/hicolor/256x256@2/apps/%{name}.png  -t %{buildroot}%{_datadir}/icons/hicolor/256x256@2/apps
install -Dm644  src-tauri/target/%{_arch}-unknown-linux-gnu/release/bundle/deb/%{name}_%{version}_%{arch2}/data/usr/share/icons/hicolor/32x32/apps/%{name}.png      -t %{buildroot}%{_datadir}/icons/hicolor/32x32/apps


%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/icons/*
%{_datadir}/completions/*


%changelog
* DATE Abdenasser Elidrissi <nasser.elidrissi065@gmail.com>
- See GitHub for full changelog 