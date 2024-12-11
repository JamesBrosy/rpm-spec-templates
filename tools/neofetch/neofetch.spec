#
# spec file for package neofetch
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

Name:           neofetch
Version:        VERSION
Release:        1%{?dist}
Summary:        CLI system information tool written in Bash

License:        MIT
URL:            https://github.com/dylanaraps/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       bash >= 3.2
Recommends:     bind-utils, catimg, coreutils, gawk, grep, pciutils

%description
Displays information about the system next to an image, the OS logo, or any
ASCII file of choice. The main purpose of Neofetch is to be used in
screenshots to show other users what OS/Distro is running, what Theme/Icons
are being used, etc.

Customizable through the use of command line flags or the user config file.
There are over 50 config options to mess around with and there's the `print_info()
function and friends which let you add your own custom info.


%prep
%autosetup
sed 's,/usr/bin/env bash,/bin/bash,g' -i neofetch

%build

%install
%make_install

%files
%{_bindir}/%{name}
%license LICENSE.md
%doc README.md CHANGELOG.md
%{_mandir}/man1/%{name}.1*

%changelog
* DATE dylanaraps <dylan.araps@gmail.com> - VERSION-1
- Updated to VERSION