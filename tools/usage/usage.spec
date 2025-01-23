#
# spec file for package usage
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}

Name:           usage
Version:        VERSION
Release:        1%{?dist}
Summary:        A spec and CLI for defining CLI tools.

License:        MIT
URL:            https://github.com/jdx/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc


%description
Usage is a spec and CLI for defining CLI tools. Arguments, flags, environment variables, and config files can all be defined in a Usage spec. It can be thought of like OpenAPI (swagger) for CLIs.

%package        bash-completion
Summary:        Bash completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)

%description    bash-completion
Bash command line completion support for %{name}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)

%description    zsh-completion
Zsh command line completion support for %{name}.

%package        fish-completion
Summary:        Fish completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)

%description fish-completion
Fish command line completion support for %{name}.

%prep
%autosetup

%build
# install toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
# build release
cargo build --release
%{name} g completion bash %{name} --usage-cmd "usage --usage-spec" > target/%{name}
%{name} g completion zsh  %{name} --usage-cmd "usage --usage-spec" > target/_%{name}
%{name} g completion fish %{name} --usage-cmd "usage --usage-spec" > target/%{name}.fish


%install
install -Dsm755 -T target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644  -T target/_%{name}        %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm644  -T target/%{name}         %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm644  -T target/%{name}.fish    %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish


%files
%license LICENSE
%{_bindir}/%{name}

%files bash-completion
%{_datadir}/bash-completion/*

%files zsh-completion
%{_datadir}/zsh/*

%files fish-completion
%{_datadir}/fish/*


%changelog
* DATE Jeff Dickey <216188+jdx@users.noreply.github.com>
- See GitHub for full changelog