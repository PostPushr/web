package com.postpushr;

import java.nio.charset.Charset;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.Security;

import org.spongycastle.jce.provider.BouncyCastleProvider;
import org.spongycastle.util.encoders.Hex;

public class Util {

	static {
		Security.insertProviderAt(new BouncyCastleProvider(), 1);
	}

	private static String Sha1Hash(String input) {
		byte[] inputByteArray = input.getBytes(Charset.forName("UTF-8"));
		MessageDigest Sha1Hasher = null;
		try {
			Sha1Hasher = MessageDigest.getInstance("SHA-1", "BC");
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (NoSuchProviderException e) {
			e.printStackTrace();
		}
		Sha1Hasher.update(inputByteArray);
		return new String(Hex.encode(Sha1Hasher.digest()));
	}

	public static String hashAndSaltPassword(String password) {
		return Util.Sha1Hash(Util.Sha1Hash(password) + Util.Sha1Hash(Secrets.getSalt()));
	}

}
