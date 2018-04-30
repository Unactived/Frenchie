# Private and sensitive informations
BLUE = 0x99e6ff
prefix = 'fr!'
# rextester
rex_url = 'http://rextester.com/rundotnet/api?LanguageChoice={}&Program={}'
rexLanguageDict = {'C#': 1, 'Vb.net': 2, 'F#': 3, 'Java': 4, 'Python2': 5, 'C': 6, 'C++': 7,
'Php': 8, 'Pascal': 9, 'Objective-c': 10, 'Haskell': 11, 'Ruby': 12, 'Perl': 13, 'Lua': 14, 'Nasm': 15,
'Sql server': 16, 'Javascript': 17, 'Lisp': 18, 'Prolog': 19, 'Go': 20, 'Scala': 21, 'Scheme': 22,
'Node.js': 23, 'Python': 24, 'Octave': 25, 'C clang': 26, 'C++ clang': 27, 'Visual c++': 28,
'Visual c': 29, 'D': 30, 'R': 31, 'Tcl': 32, 'Mysql': 33, 'Postgresql': 34, 'Oracle': 35, 'Swift': 37,
'Bash': 38, 'Ada': 39, 'Erlang': 40, 'Elixir': 41, 'Ocaml': 42, 'Kotlin': 43, 'Brainfuck': 44, 'Fortran': 45}

rexCompilerDict = {'C++': '-Wall -std=c++17 -O2 -o a.out source_file.cpp',
                   'C++ clang': '-Wall -std=c++17 -stdlib=libc++ -O2 -o a.out source_file.cpp',
                   'Visual c++': 'source_file.cpp -o a.exe /EHsc /MD /I C:\boost_1_60_0 /link /LIBPATH:C:\boost_1_60_0\stage\lib',
                   'C': '-Wall -std=gnu99 -O2 -o a.out source_file.c',
                   'C clang': '-Wall -std=gnu99 -O2 -o a.out source_file.c',
                   'Visual c': 'source_file.c -o a.exe',
                   'D': 'source_file.d -ofa.out',
                   'Go': '-o a.out source_file.go',
                   'Haskell': '-o a.out source_file.hs',
                   'Objective-c': '-MMD -MP -DGNUSTEP -DGNUSTEP_BASE_LIBRARY=1 -DGNU_GUI_LIBRARY=1 -DGNU_RUNTIME=1 -DGNUSTEP_BASE_LIBRARY=1 -fno-strict-aliasing -fexceptions -fobjc-exceptions -D_NATIVE_OBJC_EXCEPTIONS -pthread -fPIC -Wall -DGSWARN -DGSDIAGNOSE -Wno-import -g -O2 -fgnu-runtime -fconstant-string-class=NSConstantString -I. -I /usr/include/GNUstep -I/usr/include/GNUstep -o a.out source_file.m -lobjc -lgnustep-base'
                   }

# OpenWeatherMap
weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=687dd4cd7e8ae7865edef573cc3ec9f2&units=metric'
earth_url = "https://emojipedia-us.s3.amazonaws.com/thumbs/320/twitter/134/earth-globe-europe-africa_1f30d.png"

# invite
invite_url = 'https://discordapp.com/oauth2/authorize?client_id=438242027541495808&scope=bot&permissions=1194839233'

# source
source_url = 'https://github.com/FrenchMasterSword/Frenchie'
