#
# spec file for package yazi 
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}

%if 0%{?fedora}
%global vergen_git_sha Fedora
%elif 0%{?suse_version}
%global vergen_git_sha openSUSE
%elif 0%{?rhel}
%global vergen_git_sha RedHat
%else
%global vergen_git_sha %{_os}
%endif

Name:           yazi
Version:        VERSION
Release:        1%{?dist}
Summary:        Blazing fast terminal file manager written in Rust, based on async I/O
License:        MIT
Group:          Productivity/Text/Utilities
URL:            https://github.com/sxyazi/yazi
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if ! 0%{?rhel} || 0%{?rhel} > 8
Patch1:         001-system-lua.patch
%endif
Requires:       file

BuildRequires:  cargo
%if 0%{fedora} >= 42
BuildRequires:  gawk
BuildRequires:  oniguruma-devel
%endif
%if 0%{?suse_version}
BuildRequires:  lua54-devel
%else
BuildRequires:  lua-devel >= 5.4
%endif
%if ! 0%{?rhel}
BuildRequires:  ImageMagick
%endif

Suggests:       ffmpegthumbnailer
Suggests:       p7zip
Suggests:       jq
Suggests:       poppler
Suggests:       fd
Suggests:       ripgrep
Suggests:       fzf
Suggests:       zoxide
Suggests:       ImageMagick
Suggests:       wl-clipboard
Suggests:       xsel
Suggests:       chafa

%description
Yazi (means "duck") is a terminal file manager written in Rust, based on non-blocking async I/O. It aims to provide an efficient, user-friendly, and customizable file management experience.

💡 A new article explaining its internal workings: Why is Yazi Fast?

    🚀 Full Asynchronous Support: All I/O operations are asynchronous, CPU tasks are spread across multiple threads, making the most of available resources.
    💪 Powerful Async Task Scheduling and Management: Provides real-time progress updates, task cancellation, and internal task priority assignment.
    🖼️ Built-in Support for Multiple Image Protocols: Also integrated with Überzug++, covering almost all terminals.
    🌟 Built-in Code Highlighting and Image Decoding: Combined with the pre-loading mechanism, greatly accelerates image and normal file loading.
    🔌 Concurrent Plugin System: UI plugins (rewriting most of the UI), functional plugins (coming soon), custom previewer, and custom preloader; Just some pieces of Lua.
    🧰 Integration with fd, rg, fzf, zoxide
    💫 Vim-like input/select component, auto-completion for cd paths
    🏷️ Multi-Tab Support, Scrollable Preview (for videos, PDFs, archives, directories, code, etc.)
    🔄 Bulk Renaming, Visual Mode, File Chooser
    🎨 Theme System, Custom Layouts, Trash Bin, CSI u
    ... and more!


%package        bash-completion
Summary:        Bash Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description bash-completion
The official bash completion script for %{name}.

%package fish-completion
Summary:        Fish Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description fish-completion
The official fish completion script for %{name}.

%package zsh-completion
Summary:        ZSH Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description zsh-completion
The official zsh completion script for %{name}.

%prep
%autosetup -p1

%build
export YAZI_GEN_COMPLETIONS=true
export VERGEN_GIT_SHA=%{vergen_git_sha}
%if 0%{?fedora} >= 42
export RUSTONIG_SYSTEM_LIBONIG=1
%endif
cargo build --release --locked


%install
install -Dsm755 target/release/%{name}             %{buildroot}%{_bindir}/%{name}
install -Dsm755 target/release/ya                  %{buildroot}%{_bindir}/ya
install -Dm 644 yazi-boot/completions/%{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm 644 yazi-boot/completions/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dm 644 yazi-boot/completions/_%{name}     %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm 644 yazi-cli/completions/ya.bash       %{buildroot}%{_datadir}/bash-completion/completions/ya
install -Dm 644 yazi-cli/completions/ya.fish       %{buildroot}%{_datadir}/fish/vendor_completions.d/ya.fish
install -Dm 644 yazi-cli/completions/_ya           %{buildroot}%{_datadir}/zsh/site-functions/_ya

%if ! 0%{?rhel}
install -Dm 644 assets/%{name}.desktop             %{buildroot}%{_datadir}/applications/%{name}.desktop
for r in 16 24 32 48 64 128 256; do
    install -dm755 "%{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps"
    magick assets/logo.png -resize "${r}x${r}" "%{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps/yazi.png"
done
%endif

%check
export YAZI_GEN_COMPLETIONS=true
export VERGEN_GIT_SHA=%{vergen_git_sha}
%if 0%{?fedora} >= 42
export RUSTONIG_SYSTEM_LIBONIG=1
%endif
cargo test --all


%files
%license LICENSE LICENSE-ICONS
%doc README.md
%{_bindir}/%{name}
%{_bindir}/ya
%if ! 0%{?rhel}
%{_datadir}/icons/*
%{_datadir}/applications/*
%endif

%files bash-completion
%{_datadir}/bash-completion

%files fish-completion
%{_datadir}/fish

%files zsh-completion
%{_datadir}/zsh

%changelog
* DATE 三咲雅 · Misaki Masa <sxyazi@gmail.com>
- See Github for full changelog