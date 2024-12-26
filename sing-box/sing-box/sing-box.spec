#
# spec file for package sing-box
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}

%ifarch         x86_64
%define         ARCH amd64
%endif
%ifarch         aarch64
%define         ARCH arm64
%endif


Name:           sing-box
Version:        VERSION
Release:        1%{?dist}
Summary:        The universal proxy platform.

License:        GPLv3 or later
URL:            https://sing-box.sagernet.org/
Source0:        %{name}-%{version}.tar.gz

BuildRequires: git, curl, tar


%description
The universal proxy platform.


%prep
%autosetup


%build
#install go
GO_VER=$(curl -s https://raw.githubusercontent.com/actions/go-versions/main/versions-manifest.json | grep -oE '"version": "[0-9]{1}.[0-9]{1,}(.[0-9]{1,})?"' | head -1 | cut -d':' -f2 | sed 's/ //g; s/"//g')
PACKAGE="go${GO_VER}.linux-%{ARCH}.tar.gz"
SHA256SUM=$(curl -sSL https://go.dev/dl/ |grep  -A 6 -P "<td class=\"filename\"><.*>${PACKAGE}<.*>" | grep -oP '<tt>\K[^<]+')
echo "Downloading ${PACKAGE}"
curl -L -O "https://go.dev/dl/${PACKAGE}"
echo "Checking SHA256SUM"
RES=$(echo "${SHA256SUM} ${PACKAGE}" | sha256sum -c | grep -oP 'OK')
if [ $RES != 'OK' ]; then
  exit 1
  echo "An error occurred during download"
fi
tar xf ${PACKAGE}
export PATH="$(pwd)/go/bin:$PATH"

# build stable release
git checkout main

_tags=with_gvisor,with_quic,with_wireguard,with_utls,with_reality_server,with_clash_api,with_ech,with_acme,with_dhcp
CGO_ENABLED=0 go build \
    -v \
    -trimpath \
    -buildmode=pie \
    -mod=readonly \
    -modcacherw \
    -tags "$_tags" \
    -ldflags "
        -X \"github.com/sagernet/sing-box/constant.Version=%{version}\"
        -s -w -buildid=" \
    ./cmd/sing-box

sed -i "/^\[Service\]$/a StateDirectory=%{name}"    release/config/%{name}.service
sed -i "/^\[Service\]$/a StateDirectory=%{name}-%i" release/config/%{name}@.service
sed -i "/^\[Service\]$/a User=%{name}"              release/config/%{name}*.service

echo "u %{name} - \"Sing-box Service\" - -" > "release/config/%{name}.sysusers"

install -d completions
./sing-box completion bash > completions/bash
./sing-box completion fish > completions/fish
./sing-box completion zsh  > completions/zsh

echo -n \
'// Allow sing-box to set domain and default-route
polkit.addRule(function(action, subject) {
    if ((action.id == "org.freedesktop.resolve1.set-domains" ||
         action.id == "org.freedesktop.resolve1.set-default-route" ||
         action.id == "org.freedesktop.resolve1.set-dns-servers") &&
        subject.user == "sing-box") {
        return polkit.Result.YES;
    }
});' > release/config/%{name}.rules

%install
install -Dsm755 %{name}                           -t %{buildroot}%{_bindir}
install -Dm644 "release/config/config.json"       -t %{buildroot}%{_sysconfdir}/%{name}
install -Dm644 "release/config/%{name}.service"   -t %{buildroot}/usr/lib/systemd/system
install -Dm644 "release/config/%{name}@.service"  -t %{buildroot}/usr/lib/systemd/system
install -Dm644 "release/config/%{name}.sysusers"     %{buildroot}/usr/lib/sysusers.d/%{name}.conf
install -Dm644 "release/config/%{name}.rules"        %{buildroot}%{_datadir}/polkit-1/rules.d/%{name}.rules
install -Dm644 "completions/bash"                    %{buildroot}%{_datadir}/bash-completion/completions/%{name}.bash
install -Dm644 "completions/fish"                    %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dm644 "completions/zsh"                     %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -dm755 %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
/usr/lib/systemd/system/%{name}*.service
/usr/lib/sysusers.d/%{name}.conf
%dir %{_datadir}/polkit-1
%{_datadir}/polkit-1/rules.d/sing-box.rules
%dir %{_datadir}/fish
%{_datadir}/fish/*
%dir %{_datadir}/zsh
%{_datadir}/zsh/*
%dir %{_datadir}/bash-completion
%{_datadir}/bash-completion/*
%dir %{_datadir}/%{name}


%changelog
* DATE SagerNet
- See GitHub for full changelog
