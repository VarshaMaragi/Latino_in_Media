import re

non_la_countries = ['afghanistan', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bosnia and herzegowina', 'botswana', 'bouvet island', 'brazil', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african rep', 'chad', 'china', 'christmas island', 'cocos islands', 'comoros', 'congo', 'cook islands', 'cote d`ivoire', 'croatia', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'east timor', 'egypt', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french s. territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guinea', 'guinea-bissau', 'haiti', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macau', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands antilles', 'new caledonia', 'new zealand', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'papua new guinea', 'philippines', 'pitcairn', 'poland', 'portugal', 'qatar', 'reunion', 'romania', 'russian federation', 'rwanda', 'saint kitts and nevis', 'saint lucia', 'st vincent/grenadines', 'samoa', 'san marino', 'sao tome', 'saudi arabia', 'senegal', 'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'spain', 'sri lanka', 'st. helena', 'st.pierre', 'sudan', 'suriname', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'uzbekistan', 'vanuatu', 'vatican city state', 'viet nam', 'virgin islands', 'western sahara', 'yemen', 'yugoslavia', 'zaire', 'zambia', 'zimbabwe']

la_countries = ["cuba", "dominican republic","puerto rico", "costa rica", "el salvador", "guatemala", "honduras", "mexico", "nicaragua", "panama", "argentina", "bolivia", "chile", "colombia", "ecuador",  "guyana", "paraguay", "peru", "uruguay", "venezuela"]

non_la_regex = re.compile('.*afghanistan.*|.*albania.*|.*algeria.*|.*american samoa.*|.*andorra.*|.*angola.*|.*anguilla.*|.*antarctica.*|.*antigua and barbuda.*|.*armenia.*|.*aruba.*|.*australia.*|.*austria.*|.*azerbaijan.*|.*bahamas.*|.*bahrain.*|.*bangladesh.*|.*barbados.*|.*belarus.*|.*belgium.*|.*belize.*|.*benin.*|.*bermuda.*|.*bhutan.*|.*bosnia and herzegowina.*|.*botswana.*|.*bouvet island.*|.*brazil.*|.*brunei darussalam.*|.*bulgaria.*|.*burkina faso.*|.*burundi.*|.*cambodia.*|.*cameroon.*|.*canada.*|.*cape verde.*|.*cayman islands.*|.*central african rep.*|.*chad.*|.*china.*|.*christmas island.*|.*cocos islands.*|.*comoros.*|.*congo.*|.*cook islands.*|.*cote d`ivoire.*|.*croatia.*|.*cyprus.*|.*czech republic.*|.*denmark.*|.*djibouti.*|.*dominica.*|.*east timor.*|.*egypt.*|.*equatorial guinea.*|.*eritrea.*|.*estonia.*|.*ethiopia.*|.*faroe islands.*|.*fiji.*|.*finland.*|.*france.*|.*french guiana.*|.*french polynesia.*|.*french s. territories.*|.*gabon.*|.*gambia.*|.*georgia.*|.*germany.*|.*ghana.*|.*gibraltar.*|.*greece.*|.*greenland.*|.*grenada.*|.*guadeloupe.*|.*guam.*|.*guinea.*|.*guinea-bissau.*|.*haiti.*|.*hong kong.*|.*hungary.*|.*iceland.*|.*india.*|.*indonesia.*|.*iran.*|.*iraq.*|.*ireland.*|.*israel.*|.*italy.*|.*jamaica.*|.*japan.*|.*jordan.*|.*kazakhstan.*|.*kenya.*|.*kiribati.*|.*kuwait.*|.*kyrgyzstan.*|.*laos.*|.*latvia.*|.*lebanon.*|.*lesotho.*|.*liberia.*|.*libya.*|.*liechtenstein.*|.*lithuania.*|.*luxembourg.*|.*macau.*|.*macedonia.*|.*madagascar.*|.*malawi.*|.*malaysia.*|.*maldives.*|.*mali.*|.*malta.*|.*marshall islands.*|.*martinique.*|.*mauritania.*|.*mauritius.*|.*mayotte.*|.*micronesia.*|.*moldova.*|.*monaco.*|.*mongolia.*|.*montserrat.*|.*morocco.*|.*mozambique.*|.*myanmar.*|.*namibia.*|.*nauru.*|.*nepal.*|.*netherlands.*|.*netherlands antilles.*|.*new caledonia.*|.*new zealand.*|.*niger.*|.*nigeria.*|.*niue.*|.*norfolk island.*|.*northern mariana islands.*|.*norway.*|.*oman.*|.*pakistan.*|.*palau.*|.*papua new guinea.*|.*philippines.*|.*pitcairn.*|.*poland.*|.*portugal.*|.*qatar.*|.*reunion.*|.*romania.*|.*russian federation.*|.*rwanda.*|.*saint kitts and nevis.*|.*saint lucia.*|.*st vincent/grenadines.*|.*samoa.*|.*san marino.*|.*sao tome.*|.*saudi arabia.*|.*senegal.*|.*seychelles.*|.*sierra leone.*|.*singapore.*|.*slovakia.*|.*slovenia.*|.*solomon islands.*|.*somalia.*|.*south africa.*|.*spain.*|.*sri lanka.*|.*st. helena.*|.*st.pierre.*|.*sudan.*|.*suriname.*|.*swaziland.*|.*sweden.*|.*switzerland.*|.*syrian arab republic.*|.*taiwan.*|.*tajikistan.*|.*tanzania.*|.*thailand.*|.*togo.*|.*tokelau.*|.*tonga.*|.*trinidad and tobago.*|.*tunisia.*|.*turkey.*|.*turkmenistan.*|.*tuvalu.*|.*uganda.*|.*ukraine.*|.*united arab emirates.*|.*united kingdom.*|.*uzbekistan.*|.*vanuatu.*|.*vatican city state.*|.*viet nam.*|.*western sahara.*|.*yemen.*|.*yugoslavia.*|.*zaire.*|.*zambia.*|.*zimbabwe.*|')

la_regex = re.compile(".*argentina.*|.*bolivia.*|.*chile.*|.*colombia.*|.*costa rica.*|.*cuba.*|.*dominican republic.*|.*ecuador.*|.*el salvador.*|.*guatemala.*|.*guyana.*|.*honduras.*|.*mexico.*|.*nicaragua.*|.*panama.*|.*paraguay.*|.*peru.*|.*puerto rico.*|.*uruguay.*|.*venezuela.*|")

non_la_country_codes = set(['AF', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BA', 'BW', 'BV', 'BR', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CN', 'CX', 'CC', 'KM', 'CG', 'CK', 'CI', 'HR', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'TP', 'EG', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GN', 'GW', 'HT', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'FM', 'MD', 'MC', 'MN', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'AN', 'NC', 'NZ', 'NE', 'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PG', 'PH', 'PN', 'PL', 'PT', 'QA', 'RE', 'RO', 'RU', 'RW', 'KN', 'LC', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA', 'ES', 'LK', 'SH', 'PM', 'SD', 'SR', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TV', 'UG', 'UA', 'AE', 'UK', 'UZ', 'VU', 'VA', 'VN', 'VG', 'VI', 'EH', 'YE', 'YU', 'ZR', 'ZM', 'ZW'])

la_country_codes = set(['AR', 'BO', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'SV', 'GT', 'GY', 'HN', 'MX', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE'])

us_country_code = 'US'

us_states_regex = re.compile('.*indiana.*|.*new york.*|.*vermont.*|.*district of columbia.*|.*virginia.*|.*massachusetts.*|.*tennessee.*|.*oklahoma.*|.*colorado.*|.*montana.*|.*ohio.*|.*nevada.*|.*west virginia.*|.*florida.*|.*arkansas.*|.*minnesota.*|.*carolina.*|.*rhode island.*|.*new mexico.*|.*iowa.*|.*north dakota.*|.*nebraska.*|.*connecticut.*|.*missouri.*|.*mississippi.*|.*washington.*|.*south dakota.*|.*louisiana.*|.*hawaii.*|.*georgia.*|.*oregon.*|.*wisconsin.*|.*alaska.*|.*illinois.*|.*maryland.*|.*new hampshire.*|.*utah.*|.*delaware.*|.*maine.*|.*new jersey.*|.*kansas.*|.*idaho.*|.*arizona.*|.*pennsylvania.*|.*alabama.*|.*michigan.*|.*kentucky.*|.*texas.*|.*california.*|.*wyoming.*|')
