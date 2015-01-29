# Prevent brp-python-bytecompile from running
%define __os_install_post %{___build_post}

Summary: LeTOH controller app
Name: harbour-pyletoh
Version: 0.2.0
Release: 1
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: https://github.com/datakurre/harbour-pyletoh
License: GPLv3
Group: System/GUI/Other
Requires: pyotherside-qml-plugin-python3-qt5 >= 1.3.0
Requires: sailfishsilica-qt5
Requires: libsailfishapp-launcher
Requires: nemo-qml-plugin-dbus-qt5
BuildRequires: python3-base

%description
PyLeTOH controls Light emitting The Other Half

%changelog
* Thu Jan 29 2015 Asko Soukka <asko.soukka@iki.fi> - 0.2.0-1
- Add a cover action (turn leds on / off)
- Turn leds on by notifications
- Turn leds off when closing notifications
* Tue Jan 27 2015 Asko Soukka <asko.soukka@iki.fi> - 0.1.18-1
- Clean up build
* Tue Jan 27 2015 Asko Soukka <asko.soukka@iki.fi> - 0.1.11-1
- First release

%prep
%setup -q

%build

pyvenv bootstrap
bootstrap/bin/pip install requires/dist/setuptools-12.0.5.tar.gz --upgrade
bootstrap/bin/pip install requires/dist/zc.buildout-2.3.1.tar.gz
bootstrap/bin/buildout bootstrap
python3 qml/buildout buildout:install-from-cache=true
rm -rf qml/buildout lib/zc.recipe*
cat qml/app.py

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
