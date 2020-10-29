from construct import *
from construct.lib import *

#this was orignally generated from Kaitai, but didn't totally work, so it's been manually patched up, and the added to.

def xiegug90head__att_modes(subcon):
	return Enum(subcon,
		none=0,
		pre=1,
		att=2,
	)

def xiegug90head__modulations(subcon):
	return Enum(subcon,
		lsb=0,
		usb=1,
		cw=2,
		crr=3,
		nfm=4,
		fm=5,
	)

def xiegug90head__gain_modes(subcon):
	return Enum(subcon,
		false=0,
		slow=1,
		fast=2,
		auto=3,
	)



xiegug90head = Struct(
	'header' / Default(Array(2, Byte), [0x55, 0xaa]),
	'pad1' / Default(Int16ub, 0),
	
	'freq1' / Default(Int32ul, 14225000),
	'att_mode' / Default(xiegug90head__att_modes(Int8ub), 0),
	'modulation' / Default(xiegug90head__modulations(Int8ub), 1),
	'agc' / Default(xiegug90head__gain_modes(Int8ub), 0),
	'pad2' / Default(Int8ub, 0),
	'filter_high_raw' / Default(Int8ub, 100),
	'filter_low_raw' / Default(Int8ub, 4),
	#byte 14
	'pad3' / Default(Array(5, Byte), [0x00, 0x00, 0x00, 0x00, 0x00]),
	#byte 19
	'fft_scale' / Default(Int8ub, 1), #1=auto
	
	'freq2' / Default(Int32ul, 7175000),
	'att_mode2' / Default(xiegug90head__att_modes(Int8ub), 0),
	'modulation2' / Default(xiegug90head__modulations(Int8ub), 0),
	'agc2' / Default(xiegug90head__gain_modes(Int8ub), 0),
        'pad2b' / Default(Int8ub, 0),
	'filter_high_raw2' / Default(Int8ub, 100),
	'filter_low_raw2' / Default(Int8ub, 4),
	#30
	'pad5' / Default(Array(5, Byte), [0x00,0x00,0x00,0x00,0x00]),
	'fft_scale2' / Default(Int8ub, 1), #1=auto
	
	'ctrl1' / Default( BitStruct(
          'transmit' / Flag, #0x80
          'mem_en' / Flag,
          'tuner_en' / Flag,
          'nb_en' / Flag,
          'mic_compression' / Flag,
          'output_headphones' / Flag,
          'split_en' / Flag,
          'panel_lock' / Flag,
	), {'transmit':False, "mem_en":False, "tuner_en":False, "nb_en":False, "mic_compression":False, "output_headphones":False, "split_en":False, "panel_lock":False }),
        #37
        'ctrl2' / Default(BitStruct(
          'shutdown_req' / Flag, # not sure, just observed right before powerdown
          Padding(1),
          'tuning' / Flag, #0x20
          Padding(5),
	), {'shutdown_req':False, 'tuning':False }),
        #38
        'ctrl3' / Default( BitStruct(
          'rclk_raw_low' / BitsInteger(3),
          'cw_disp_en' / Flag,
          'vox_en' / Flag,
          'audio_in_line_en' / Flag,
          'tx_disable' / Flag,
          'cw_qsk' / Flag,
	), {'rclk_raw_low':0, 'cw_disp_en':False, 'vox_en': False, 'audio_in_line_en':False, 'tx_disable':True, 'cw_qsk':True }),
        'rclk_raw_high' / Default(Int8ub, 125),
        
        'ctrl4' / Default( BitStruct(
          #40
          'vox_anti_gain_low' / BitsInteger(1),
          'vox_gain' / BitsInteger(7),
          #41
          'vox_delay_low' / BitsInteger(2),
          'vox_anti_gain_high' / BitsInteger(6),
          #42
          'gain_low' / BitsInteger(5),
          'vox_delay_high' / BitsInteger(3),
          #
          Padding(4),
          'beep_en' / Flag,
          'band_stack_full' / Flag,
          'gain_high' / BitsInteger(2),
        ), {'vox_anti_gain_low':0, 'vox_gain':0, 'vox_delay_low': 0, 'vox_anti_gain_high':0, 'gain_low':15, 'vox_delay_high':0, 'beep_en':True, 'band_stack_full':False, 'gain_high':0 }),
        #44
        'rf_power' / Default(Int8ub,1),
        'sql_level' / Default(Int8ub,0),
        'ctrl5' / Default( BitStruct(
          'nb_level' / BitsInteger(4),
          'nb_width' / BitsInteger(4),          
	), {'nb_level':3, 'nb_width':3 }),
        Padding(1),
        #48
        'volume' /  Default(Int8ub,1), #0-28
        'mic_gain' / Default(Int8ub,10), #0-20
        'unknown1' / Default(Byte, 0x50),
        'cq_qsk_time_raw' / Default(Int8ub,2), #0-20
        'unknown2' / Default(Byte, 0x01),
        'mem_ch' / Default(Int8ub,6), #0-20
        #54
        'ctrl6' / Default(BitStruct(
          Padding(7),
          'vfo_b_en' / Flag,
	), {'vfo_b_en':False}),
        Padding(1),
        'unknown3' / Default(Array(4, Byte), [0xff, 0xff, 0xff, 0xff]),
        #60
        'cw_wpm' / Default(Int8ub,10), #5-50 wpm
        'ctrl7' / Default( BitStruct(
          'cw_ratio_raw' / BitsInteger(4),
          Padding(1),
          'cw_mode_b' / Flag,
          'cw_mlr' / BitsInteger(2),
	), {'cw_ratio_raw':0, 'cw_mode_b':False, 'cw_mlr': 1}),
        #Padding(20),
        'unknown4' / Default(Array(20, Byte), [0xff, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x1f, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32]),
        #82
        'ctrl8' / Default( BitStruct(
          Padding(4),
          'swr_threshold_raw' / BitsInteger(4),
          'aux_out_vol' / BitsInteger(4),
          'aux_in_vol' / BitsInteger(4),
        ), {'swr_threshold_raw':1, 'aux_out_vol':9, 'aux_in_vol': 8}),
        #84
        'ctrl9' / Default( BitStruct(
          'ritval_low' / BitsInteger(8),
          Padding(6),
          'ritval_high' / BitsInteger(2),
        ), {'ritval_low':0, 'ritval_high':0}),
        'unknown5' / Default(Array(6, Byte), [0xff, 0xff, 0x00, 0x00, 0x00, 0x00]),
        'checksum' / Default(Int32ul,0),
        
        #computed
	'filter_low' / Computed( (100 + (this.filter_low_raw * 25))),
	'filter_high' / Computed( (125 + (this.filter_high_raw * 25))),
	'rclk_tune' / Computed(( (this.rclk_raw_high << 3) + this.ctrl3.rclk_raw_low) - 1000 ),
	'vox_anti_gain'  / Computed( ((this.ctrl4.vox_anti_gain_high << 1) + this.ctrl4.vox_anti_gain_low) ),
	'vox_delay'  / Computed( ((this.ctrl4.vox_delay_high << 2) + this.ctrl4.vox_delay_low) /10. ),
	'gain'  / Computed( ((this.ctrl4.gain_high << 5) + this.ctrl4.gain_low) ),
	'cw_qsk_time' / Computed( ((this.cq_qsk_time_raw * 100))),
	'cw_ratio' / Computed( ( 2 + (this.ctrl7.cw_ratio_raw /10.))),
	'swr_threshold' / Computed( ( 1.8 + (this.ctrl8.swr_threshold_raw *0.2))),
	'ritval1'  / Computed( ((((this.ctrl9.ritval_high *256) + this.ctrl9.ritval_low) +512)%1024)-512),
	
)

_schema = xiegug90head
