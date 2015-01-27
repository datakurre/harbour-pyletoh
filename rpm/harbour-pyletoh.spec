# Prevent brp-python-bytecompile from running
%define __os_install_post %{___build_post}

Summary: LeTOH controller app
Name: harbour-pyletoh
Version: 0.1.2
Release: 1
Source: %{name}-%{version}.tar.gz
BuildArch: armv7hl
URL: https://github.com/datakurre/harbour-pyletoh
License: GPLv3
Group: System/GUI/Other
Requires: pyotherside-qml-plugin-python3-qt5 >= 1.3.0
Requires: sailfishsilica-qt5
Requires: libsailfishapp-launcher

%description
PyLeTOH controls Light emitting The Other Half

%prep
%setup -q

%build

python3 bootstrap.py
python3 qml/buildout

%install

TARGET=%{buildroot}/%{_datadir}/%{name}
mkdir -p $TARGET
cp -rpv qml $TARGET/
cp -rpv lib $TARGET/

TARGET=%{buildroot}/%{_datadir}/applications
mkdir -p $TARGET
cp -rpv %{name}.desktop $TARGET/

TARGET=%{buildroot}/%{_datadir}/icons/hicolor/86x86/apps/
mkdir -p $TARGET
cp -rpv %{name}.png $TARGET/

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
