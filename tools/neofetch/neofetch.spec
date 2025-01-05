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
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       bash >= 3.2
Recommends:     bind-utils, catimg, coreutils, gawk, grep, pciutils

%description
Neofetch displays information about your system next to an image, your OS logo, or any ASCII file of your choice. The main purpose of Neofetch is to be used in screenshots to show other users what OS/distribution you're running, what theme/icons you're using and more.


%prep
%autosetup
sed 's,/usr/bin/env bash,/bin/bash,g' -i neofetch

%build

%install
install -Dm755 %{name}   -t %{buildroot}%{_bindir}
install -Dm644 %{name}.1 -t %{buildroot}%{_mandir}/man1

%files
%{_bindir}/%{name}
%license LICENSE.md
%doc README.md
%{_mandir}/man1/%{name}.1*

%changelog
* DATE dylanaraps <dylan.araps@gmail.com> - VERSION-1
- Updated to VERSION
