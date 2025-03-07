%define _fortify_level 2

%define         pkgname             scrcpy
%global         forgeurl            https://github.com/Genymobile/%{pkgname}
Version:        3.1

%forgemeta -i

Name:           %{pkgname}
Release:        2%{?dist}
Summary:        Display and control your Android device
License:        ASL 2.0

URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://github.com/Genymobile/%{pkgname}/releases/download/v%{version}/%{pkgname}-server-v%{version}

BuildRequires:  meson gcc
BuildRequires:  java-devel >= 11
BuildRequires:  desktop-file-utils

BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(ffms2)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  vulkan-loader

Requires:       android-tools

# https://github.com/Genymobile/scrcpy/blob/master/FAQ.md#issue-with-wayland
Recommends:     libdecor

%description
This application provides display and control of Android devices
connected on USB (or over TCP/IP).

%package        bash-completion
Summary:        Bash completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description    bash-completion
Bash command line completion support for %{name}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}
Requires:       zsh
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description    zsh-completion
Zsh command line completion support for %{name}.

%prep
%forgeautosetup -p1

%build
%meson -Db_lto=true -Dprebuilt_server='%{S:1}'
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{pkgname}{,-console}.desktop

%files
%license LICENSE
%doc README.md FAQ.md
%{_bindir}/%{pkgname}
%{_datadir}/%{pkgname}
%{_mandir}/man1/%{pkgname}.1*
%{_datadir}/icons/hicolor/*/apps/%{pkgname}.png
%{_datadir}/applications/*.desktop

%files bash-completion
%{_datadir}/bash-completion/completions/%{pkgname}

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{pkgname}